#include <avr/io.h>

#define led1 PB0
#define led2 PB1

int main(void)
{
    /* Replace with your application code */
	DDRB|=(1<<led1)|(1<<led2);
	TCCR1B|=(1<<CS10)|(1<<CS11);
    while (1) 
    {
		if(TCNT1>2232)
		{
			TCNT1=0;
			PORTB^=(1<<led1);//blink every 7th of a second
		}
		if(TCNT0>15625)
		{
			TCNT0=0;
			PORTB^=(1<<led2);//blink every second
		}
		
    }
}

