#include <avr/io.h>
#include <util/delay.h>

#define switchportpin PINA
#define switchpin PA0
#define led PB0
int button_down;

void debounce(unsigned char portbit, unsigned char portpin)
{
	int count = 0;
	int button_state = 0;
	int current_state = (~portpin & (1<<portbit)) != 0;
	if (current_state != button_state) 
	{
		count++;
		if (count >= 500) 
		{
			button_state = current_state;
			if (current_state != 0) 
			{
				button_down = 1;
			}
			count = 0;
		}
	} 
	else 
	{
		count = 0;
	}
}
int main()
{
	PORTA |= (1<<switchpin);
	DDRB |= (1<<led);
	while(1)
	{
	    debounce(switchpin, switchportpin);
		if (button_down)
		{
			button_down = 0;
			PORTB ^= (1<<led);
		}
    }
	return 0;
}
