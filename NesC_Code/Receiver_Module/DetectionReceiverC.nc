/*

	Codice generale del sistema di allarme, lato Ricevitore
*/


#include "printf.h"
#include "Message.h"

module DetectionReceiverC {

	uses{
		interface Boot;
	 	interface Leds;
		
		//interface Timer<TMilli> as Timer;
	 	interface SplitControl as Radio;
		interface Packet;
		interface AMPacket;
		interface Receive; 
	}
}

implementation {
	
	bool radioON = FALSE;
	bool busy = FALSE;

	event void Boot.booted(){
		call Radio.start(); 
	}
	
	event void Radio.startDone(error_t err) {
		if(err == SUCCESS) {
			call Leds.led0On();
			radioON = TRUE; 	
		}
		else {
			call Radio.start();
		}

	}
	
	
	// RADIO 
	event message_t* Receive.receive(message_t *msg, void* payload, uint8_t len) {

		if (len == sizeof(MessageStr)) {
			
			MessageStr* packet_in = (MessageStr*) payload;
			
			uint8_t door_state = packet_in->door_state ;
			uint8_t window_state = packet_in->window_state;
			uint8_t PIR_state = packet_in->PIR_state;
			
			uint16_t lux = packet_in->lux;
			uint16_t temperature = packet_in->temperature;
			uint16_t humidity_r = packet_in->humidity_r;
			
			call Leds.led2On();
	
			printf("%d\n", door_state);
			printfflush();	
			printf("%d\n", window_state);
			printfflush();
			printf("%d\n", PIR_state);
			printfflush();		
			printf("%d\n", lux);
			printfflush();	
			printf("%d\n", temperature);
			printfflush();	
			printf("%d\n", humidity_r);
			printfflush();	
	
			//busy = TRUE;
		}

		return msg;
		//call Radio.stop();
	}

	event void Radio.stopDone(error_t err) {
		if (err == SUCCESS)
			call Leds.led0Off();
	}	
}

