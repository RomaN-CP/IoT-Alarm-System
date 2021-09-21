/*

	Codice generale del sistema di allarme, lato trasmettitore
*/

#include "math.h"
#include "Message.h"

module DetectionSenderC {

	uses{
		interface Boot;
		interface Leds;
		
		interface Timer<TMilli> as Detection_Timer;
		interface Timer<TMilli> as Sensing_Timer;

		interface Read<uint16_t> as Temperature;
		interface Read<uint16_t> as Humidity;
		interface Read<uint16_t> as Light;
	
	 	interface SplitControl as Radio;
		interface Packet;
		interface AMPacket;
		interface AMSend; 

		interface HplMsp430GeneralIO as out_door;
		interface HplMsp430GeneralIO as in_door;
		interface HplMsp430GeneralIO as out_window;
		interface HplMsp430GeneralIO as in_window;
		interface HplMsp430GeneralIO as in_PIR;
	}

}

implementation {
	
	// Sensing Variables
	uint16_t dataCelsius = 0;
	uint16_t dataHumidity = 0;
	uint16_t relHumidity = 0;
	uint16_t dataLight = 0;

	
	uint16_t lux, humidity_r, temperature;
	

	//GPIO variables  
	uint8_t PIR_state=0;
	uint8_t door_state=0;
	uint8_t window_state=0;
	bool alarm = FALSE;
	uint8_t state=0;

	bool PIR_bool ;
	bool door_bool ;
	bool window_bool ;
		
	bool radioON = FALSE;
	bool busy = FALSE;

	message_t _pkt;
	
	event void Boot.booted(){
		// setting gpio pin 
		
		call in_door.makeInput();
		call in_window.makeInput();
		call in_PIR.makeInput();			

		call out_door.makeOutput();
		call out_window.makeOutput();
		call out_door.set();
		call out_window.set();
		
		

		call Sensing_Timer.startPeriodic(5*1024);
		call Detection_Timer.startPeriodic(1024);

	}
	
	// Sensing
	event void Sensing_Timer.fired() {
		call Temperature.read();
		call Humidity.read();
		call Light.read();
		
	}

	event void Temperature.readDone( error_t code , uint16_t data){	
		if (code == SUCCESS) {
			dataCelsius = -39+0.01*data;
			temperature = dataCelsius;
		}
	}
	
	event void Humidity.readDone( error_t code , uint16_t data){
		if (code == SUCCESS){
			dataHumidity = -2.0468+0.0367*data-15955*0.000001*sqrtf(data);
			relHumidity = (dataCelsius - 25)*(0.01+0.00008*dataHumidity)+dataHumidity;
			humidity_r= relHumidity;
		}
	}

	event void Light.readDone( error_t code , uint16_t data){
		if(code == SUCCESS){
			dataLight = 2.28881*data;
			lux = dataLight;
		}
	}
	
	// DETECTION	
	event void Detection_Timer.fired() {

		call Radio.start();

		PIR_bool = call in_PIR.get();
		window_bool= call in_window.get();
		door_bool = call in_door.get();
		
		if (door_bool == FALSE) {
				call Leds.led2On();  //LED BLU ON
				door_state = 0;
			}
			else {
				call Leds.led2Off();
				door_state=1;

			}
			if (window_bool == FALSE) {
				call Leds.led1On();
				window_state=0;
			}
			else {
				call Leds.led1Off();
				window_state=1;

			}
			if (PIR_bool == FALSE) {
				call Leds.led0On();
				PIR_state=0;
			}
			else {
				call Leds.led0Off();
				PIR_state=1;
			}
	}
		
	// RADIO 
	event void Radio.startDone(error_t err) {
		if(err == SUCCESS) {
			radioON = TRUE; 	
			if (!busy && radioON) {

					MessageStr* msg = call Packet.getPayload(& _pkt, sizeof(MessageStr));
					
					msg->lux = lux;
					msg->temperature = temperature;
					msg->humidity_r = humidity_r;
					msg->door_state = door_state;
					msg->window_state = window_state;
					msg->PIR_state = PIR_state;

			if (call AMSend.send(AM_BROADCAST_ADDR, & _pkt, sizeof(MessageStr)) == SUCCESS) {
				busy = TRUE;
				}
			}
		}
		else {
			call Radio.start();
		
		}

	}

	event void AMSend.sendDone(message_t* msg, error_t error){
		if (error == SUCCESS){
			busy = FALSE;
			call Radio.stop();
		}
		
	}
	
	event void Radio.stopDone(error_t error) {}

	
}

