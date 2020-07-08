#include <avr/io.h>
#include <avr/interrupt.h>

#define led PB0

int main(void)
{
	sei();
	DDRB|=(1<<PB0);
	TCCR1B|=(1<<CS10)|(1<<CS11)|(1<<WGM12);
	TIMSK|=(1<<OCIE1B);
	OCR1B=15624; //toggle led every second
    /* Replace with your application code */
    while (1) 
    {
    }
}

ISR(TIMER1_COMPB_vect)
{
	PORTB^=(1<<led);
}

