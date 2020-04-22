#include <iostream>
#include <ros/ros.h>
#include <pcl_ros/point_cloud.h>
#include <sensor_msgs/PointCloud2.h>
#include <pcl_conversions/pcl_conversions.h>
#include <pcl/ModelCoefficients.h>
#include <pcl/io/pcd_io.h>
#include <pcl/point_types.h>
#include <pcl/sample_consensus/method_types.h>
#include <pcl/sample_consensus/model_types.h>
#include <pcl/segmentation/sac_segmentation.h>
#include <pcl/filters/voxel_grid.h>
#include <pcl/filters/extract_indices.h>
#include <pcl/features/integral_image_normal.h>
#include <pcl/segmentation/organized_multi_plane_segmentation.h>


ros::Publisher pub;

void 
cloud_cb (const pcl::PCLPointCloud2ConstPtr& cloud_blob)
{
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_outliers (new pcl::PointCloud<pcl::PointXYZ>), cloud (new pcl::PointCloud<pcl::PointXYZ>);

  // Convert to the templated PointCloud
  pcl::fromPCLPointCloud2 (*cloud_blob, *cloud);

  //Normal estimation
  pcl::IntegralImageNormalEstimation<pcl::PointXYZ, pcl::Normal> ne;
  ne.setNormalEstimationMethod (ne.COVARIANCE_MATRIX);
  ne.setMaxDepthChangeFactor (0.03f);
  ne.setNormalSmoothingSize (20.0f);

  pcl::PointCloud<pcl::Normal>::Ptr normal_cloud (new pcl::PointCloud<pcl::Normal>);
  normal_cloud->clear();

  ne.setInputCloud(cloud);
  ne.compute(*normal_cloud);
  
  pcl::OrganizedMultiPlaneSegmentation<pcl::PointXYZ, pcl::Normal, pcl::Label> mps;
  //mps.setMinInliers (500);
  mps.setAngularThreshold (0.017453 * 2.0); //60 degrees
  mps.setDistanceThreshold (0.02); //2cm

  std::vector<pcl::PlanarRegion<pcl::PointXYZ>,   Eigen::aligned_allocator<pcl::PlanarRegion<pcl::PointXYZ> > > regions;
  pcl::PointCloud<pcl::PointXYZ>::Ptr contour (new pcl::PointCloud<pcl::PointXYZ>);
  std::vector<pcl::ModelCoefficients> model_coefficients;
  std::vector<pcl::PointIndices> inlier_indices;
  pcl::PointCloud<pcl::Label>::Ptr labels (new pcl::PointCloud<pcl::Label>);
  std::vector<pcl::PointIndices> label_indices;
  std::vector<pcl::PointIndices> boundary_indices;

  regions.clear();

  mps.setInputNormals(normal_cloud);
  mps.setInputCloud(cloud);
  mps.segmentAndRefine(regions, model_coefficients, inlier_indices, labels, label_indices, boundary_indices);

  pcl::ExtractIndices<pcl::PointXYZ> extract;
  std::cout<<inlier_indices.size()<<std::endl;
  cloud_outliers=cloud;
  for (int i= 0; i!= inlier_indices.size(); i++) 
  {
	  extract.setInputCloud(cloud_outliers);
  	  pcl::PointIndices::Ptr ptr (new pcl::PointIndices);
          pcl::PointIndices a=inlier_indices[i];
          *ptr=a;
	  extract.setIndices(ptr);
	  extract.setNegative(true);  // Extract the outliers
	  extract.filter(*cloud_outliers);
  }

  pub.publish (*cloud_outliers);
}

int
main (int argc, char** argv)
{
  // Initialize ROS
  ros::init (argc, argv, "obstacles");
  ros::NodeHandle nh;

  // Create a ROS subscriber for the input point cloud
  ros::Subscriber sub = nh.subscribe ("input", 1, cloud_cb);

  // Create a ROS publisher for the output point cloud
  pub = nh.advertise<sensor_msgs::PointCloud2> ("output", 1);

  // Spin
  ros::spin ();
}



  

