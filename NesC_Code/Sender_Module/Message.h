#ifndef MESSAGE_H
#define MESSAGE_H

enum {
	AM_MESSAGE = 50
};

typedef nx_struct MessageStr {
	
	nx_uint8_t door_state;
	nx_uint8_t window_state;
	nx_uint8_t PIR_state;

	nx_uint16_t lux;
	nx_uint16_t temperature;
	nx_uint16_t humidity_r;

} MessageStr;

#endif
