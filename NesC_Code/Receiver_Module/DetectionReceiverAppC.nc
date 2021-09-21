/*

	Configuration File Receiver
*/

configuration DetectionReceiverAppC {}

implementation {
	
	components DetectionReceiverC, MainC, LedsC;
	//components new TimerMilliC() as Timer;
	components ActiveMessageC;
	components new AMReceiverC(AM_MESSAGE);

	//components PrintfC , SerialStartC;
	components SerialPrintfC, SerialStartC;

	DetectionReceiverC.Boot -> MainC; 
	DetectionReceiverC.Leds -> LedsC;
	//DetectionReceiverC.Timer -> Timer;

	DetectionReceiverC.Radio -> ActiveMessageC;
	DetectionReceiverC.Receive -> AMReceiverC;
	DetectionReceiverC.Packet -> AMReceiverC;
	DetectionReceiverC.AMPacket -> AMReceiverC;
}


