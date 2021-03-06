#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "nas_msg_parser.h"


static void test_call_back(lte_nas_msg_t msg_type, unsigned int msg_ie_id, unsigned int info_id, unsigned char *info, unsigned short len){
    printf("MSG %s(0x%x)\n    IE %s(%d)\n    INFO %s(%d)\n    VALUE ", nas_msg_type_to_str(msg_type), msg_type, nas_msg_ie_id_to_str(msg_type, msg_ie_id), msg_ie_id, nas_msg_ie_info_id_to_str(msg_type, msg_ie_id, info_id), info_id);
    while(len){
        printf("0x%x ", *info);
        info++;
        len--;
    }
    printf("\n");
}

unsigned char test_data[] = {
    0x07 ,0x41 ,0x03 ,0x0B ,0xF6 ,0x21 ,0x13 ,0x23 ,0x00 ,0x00 ,
    0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x08 ,0x00 ,0x00 ,0x00 ,0x00 ,
    0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x01 ,0x11 ,0x19 ,0x00 ,0x00 ,
    0x00 ,0x50 ,0x0B ,0xF6 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,0x00 ,
    0x00 ,0x00 ,0x00 ,0x00 ,0x52 ,0x21 ,0x13 ,0x23 ,0xFF ,0xFE ,0xD0
    };

int main(int argc, char *argv[]){

    nas_msg_parse(test_data, sizeof(test_data), test_call_back);

    return 0;
}
