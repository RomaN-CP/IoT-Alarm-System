		

configuration DetectionSenderAppC {}

implementation {
	
	components MainC, LedsC, DetectionSenderC;
	components new TimerMilliC() as Sensing_Timer;
	components new TimerMilliC() as Detection_Timer;
		
	components HplMsp430GeneralIOC;
	
	components ActiveMessageC;
	components new AMSenderC(AM_MESSAGE);
	
	components new SensirionSht11C() as TemperatureDriver;
	components new SensirionSht11C() as HumidityDriver;
	components new HamamatsuS1087ParC() as LightDriver;	

	DetectionSenderC.Boot -> MainC;
	DetectionSenderC.Leds -> LedsC;
	DetectionSenderC.Sensing_Timer -> Sensing_Timer;
	DetectionSenderC.Detection_Timer -> Detection_Timer;

	//PORTA	

	DetectionSenderC.out_door -> HplMsp430GeneralIOC.Port63;  			//PIN 10 
	DetectionSenderC.in_door -> HplMsp430GeneralIOC.Port23;   			//GIO2 PIN3 U28
	
	//FINESTRA
	DetectionSenderC.out_window -> HplMsp430GeneralIOC.Port61; 			//ADC1 PIN5 U2
	DetectionSenderC.in_window -> HplMsp430GeneralIOC.Port67;			//DMAE0 PIN4 U28 GIO3
	
	//PIR
	DetectionSenderC.in_PIR -> HplMsp430GeneralIOC.Port60; 				//GIO4 SCL pin 6 U2

	DetectionSenderC.Radio -> ActiveMessageC;		
	DetectionSenderC.Packet -> AMSenderC;
	DetectionSenderC.AMPacket -> AMSenderC;
	DetectionSenderC.AMSend -> AMSenderC;
	
	DetectionSenderC.Temperature -> TemperatureDriver.Temperature;
	DetectionSenderC.Humidity -> HumidityDriver.Humidity;
	DetectionSenderC.Light -> LightDriver;

}

