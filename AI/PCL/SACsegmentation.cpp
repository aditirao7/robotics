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


ros::Publisher pub;

void 
cloud_cb (const sensor_msgs::PointCloud2ConstPtr& input)
{
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_inliers (new pcl::PointCloud<pcl::PointXYZ>), cloud_outliers (new pcl::PointCloud<pcl::PointXYZ>), cloud (new pcl::PointCloud<pcl::PointXYZ>);
  pcl::ModelCoefficients::Ptr plane (new pcl::ModelCoefficients);
  pcl::PointIndices::Ptr inliers_plane (new pcl::PointIndices);
  pcl::PointCloud<pcl::PointXYZ>::Ptr cloud_plane (new pcl::PointCloud<pcl::PointXYZ>);

  // Convert to the templated PointCloud
  pcl::fromROSMsg(*input, *cloud);

  // Create the segmentation object
  pcl::SACSegmentation<pcl::PointXYZ> seg;

  // Optional
  seg.setOptimizeCoefficients (true);

  // Mandatory
  seg.setModelType (pcl::SACMODEL_PLANE);
  seg.setMethodType (pcl::SAC_RANSAC);
  seg.setMaxIterations (500);
  seg.setDistanceThreshold (0.02);
  Eigen::Vector3f axis = Eigen::Vector3f(0.0,1.0,0.0); //y axis
  seg.setAxis(axis);
  seg.setEpsAngle(  80.0f * (M_PI/180.0f) );
  seg.setInputCloud(cloud);
  seg.segment (*inliers_plane, *plane); 

  //Extracting
  pcl::ExtractIndices<pcl::PointXYZ> extract;
  extract.setInputCloud (cloud);
  extract.setIndices (inliers_plane);           
  extract.setNegative (true);  // Extract the outliers
  extract.filter (*cloud_outliers); 

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

