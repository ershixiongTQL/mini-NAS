#include "nas_ie_ue_radio_capability_id_availability.h"


struct ue_radio_capability_id_availablity{
	union{
			unsigned char octet;
			struct{
#if __BYTE_ORDER == __BIG_ENDIAN
				unsigned char ue_rcra : 3, //UE radio capability ID availability value
							  spare : 5;
#else
				unsigned char spare : 5,
							  ue_rcra : 3;
#endif
				}m;
			}u;
};

static void parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv){

	struct ue_radio_capability_id_availablity *ie = (struct ue_radio_capability_id_availablity *)data;

#ifdef CARE_UE_RADIO_CAPABILITY_ID_AVAILABILITY_UE_RCIDAV
	noticer((unsigned int)UE_RCIDAV, (unsigned char *)&(ie->u.octet));
#endif

}

void nas_ie_ue_radio_capability_id_availability_parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv){

	parse(data, len, noticer, priv);

}
const char *nas_ie_ue_radio_capability_id_availability_info_id_to_str(unsigned int id){

	switch(id){
		case UE_RCIDAV:
			return "UE radio capability ID availability value";
		default:
			return "?";
	}
}






