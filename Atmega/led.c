#include <asf.h>
#include <avr/io.h>
#include <avr/delay.h>
#define LED 4

int main (void)
{
	DDRB|=(1<<LED);
	while(1)
	{
		PORTB^=(1<<LED);
		_delay_ms(100);
	}
}
