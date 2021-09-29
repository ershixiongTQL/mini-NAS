#include "nas_ie_ue_network_capability.h"


typedef struct ue_network_capability{

	uint8_t eea; //EPS encryption algorithms(octet 3)
	uint8_t eia; //EPS integrity algorithms(octet 4)
	uint8_t uea; //UMTS encryption algorithms(octet 5)
	union{
		uint8_t octet6;
		struct{
#if __BYTE_ORDER == __BIG_ENDIAN
			uint8_t uia : 7, //UMTS integrity algorithms
					ucs2 : 1; //UCS2
#else
			uint8_t ucs2 : 1,
					uia : 7; 
#endif
		}m;
	}u6;

	union{
		uint8_t octet7;
		struct{
#if __BYTE_ORDER == __BIG_ENDIAN
			uint8_t nf : 1,
					vcc : 1,
					lcs : 1,
					lpp : 1,
					acc : 1,
					ash : 1,
					prose : 1,
					prose_dd : 1;
#else
			uint8_t prose_dd : 1,
					prose : 1,
					ash : 1,
					acc : 1,
					lpp : 1,
					lcs : 1,
					vcc : 1,
					nf : 1;
#endif
		}m;

	}u7;
	union{
		uint8_t octet8;
		struct{
#if __BYTE_ORDER == __BIG_ENDIAN
			uint8_t prose_dc : 1,
					prose_relay : 1,
					cp_ciot : 1,
					up_ciot : 1,
					s1u_data : 1,
					erwOpdn : 1,
					hccp_ciot : 1,
					epco : 1;
#else
			uint8_t epco : 1,
					hccp_ciot : 1,
					erwOpdn : 1,
					s1u_data : 1,
					up_ciot : 1,
					cp_ciot : 1,
					prose_relay : 1,
					prose_dc : 1;

#endif
		}m;
	}u8;

	union{
		uint8_t octet9;
		struct{
#if __BYTE_ORDER == __BIG_ENDIAN
			uint8_t mult_edrb : 1,
					v2xpc5 : 1,
					restric_tec : 1,
					cp_backoff : 1,
					dcnr : 1,
					n1mode : 1,
					sgc : 1,
					L5_bearers : 1;
#else
			uint8_t L5_bearers : 1,
					sgc : 1,
					n1mode : 1,
					dcnr : 1,
					cp_backoff : 1,
					restric_tec : 1,
					v2xpc5 : 1,
					mult_edrb : 1;
#endif
		}m;
	}u9;

	union{
		uint8_t octet10;
		struct{
#if __BYTE_ORDER == __BIG_ENDIAN
			uint8_t racs : 1,
					wusa : 1,
					cp_mt_edt : 1,
					up_mt_edt : 1,
					v2x_nrpc5 : 1,
					spare : 3;
#else
			uint8_t spare : 3,
					v2x_nrpc5 : 1,
					up_mt_edt : 1,
					cp_mt_edt : 1,
					wusa : 1,
					racs : 1;

#endif
		}m;
	}u10;
	
	uint8_t spare[5];
}ue_network_capability_t;

static void parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv)
{
	unsigned char val;
	unsigned int pos = 0;
	struct ue_network_capability *ie = (struct ue_network_capability *)data;

	//all parser
	POS_LEN_COMP(len, ++pos);
#ifdef CARE_UE_NETWORK_CAPABILITY_EEA
	val = ie->eea;
	noticer((unsigned int)EEA, (unsigned char *)&val, sizeof(val), priv);
#ifdef UE_NETWORK_CAPABILITY_SHOW_DETAILS
	nasEEA2Str(val);
#endif
#endif

	POS_LEN_COMP(len, ++pos);
#ifdef CARE_UE_NETWORK_CAPABILITY_EIA
	val = ie->eia;
	noticer((unsigned int)EIA, (unsigned char *)&val, sizeof(val), priv);
#ifdef UE_NETWORK_CAPABILITY_SHOW_DETAILS
	nasEIA2Str(val);
#endif
#endif

	POS_LEN_COMP(len, ++pos);
#ifdef CARE_UE_NETWORK_CAPABILITY_UEA
	val = ie->uea;
	noticer((unsigned int)UEA, (unsigned char *)&val, sizeof(val), priv);
#ifdef UE_NETWORK_CAPABILITY_SHOW_DETAILS
	nasUEA2Str(val);
#endif
#endif

	POS_LEN_COMP(len, ++pos);
#ifdef CARE_UE_NETWORK_CAPABILITY_UIAANDUCS2
	val = ie->u6.octet6;
	noticer((unsigned int)UIAAndUCS2, (unsigned char *)&val, sizeof(val), priv);
#ifdef UE_NETWORK_CAPABILITY_SHOW_DETAILS
	nasUIAandUCS2ToStr(val);
#endif
#endif
	
	POS_LEN_COMP(len, ++pos);
#ifdef CARE_UE_NETWORK_CAPABILITY_OCTET7
	val = ie->u7.octet7;
	noticer((unsigned int)OCTET7, (unsigned char *)&val, sizeof(val), priv);
#ifdef UE_NETWORK_CAPABILITY_SHOW_DETAILS
	nasOctet7ToStr(val);
#endif
#endif
	
	POS_LEN_COMP(len, ++pos);
#ifdef CARE_UE_NETWORK_CAPABILITY_OCTET8
	val = ie->u8.octet8;
	noticer((unsigned int)OCTET8, (unsigned char *)&val, sizeof(val), priv);
#ifdef UE_NETWORK_CAPABILITY_SHOW_DETAILS
	nasOctet8ToStr(val);
#endif
#endif
	

	POS_LEN_COMP(len, ++pos);
#ifdef CARE_UE_NETWORK_CAPABILITY_OCTET9
	noticer((unsigned int)OCTET9, (unsigned char *)&val, sizeof(val), priv);
#ifdef UE_NETWORK_CAPABILITY_SHOW_DETAILS
	nasOctet9ToStr(val);
#endif
#endif
	
	POS_LEN_COMP(len, ++pos);
#ifdef CARE_UE_NETWORK_CAPABILITY_OCTET7
	val = ie->u10.octet10;
	noticer((unsigned int)OCTET10, (unsigned char *)&val, sizeof(val), priv);
#ifdef UE_NETWORK_CAPABILITY_SHOW_DETAILS
	nasOctet10ToStr(val);
#endif
#endif

}

void nas_ie_ue_network_capability_parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv){
	//printf("\n\t%s[%d]\n", __FUNCTION__, __LINE__);
    parse(data, len, noticer, priv);
}

const char *nas_ie_ue_network_capability_info_id_to_str(unsigned int id){
    switch(id){
        case EEA: return "EEA";
        case EIA: return "EIA";
		case UEA: return "UEA";
		case UIAAndUCS2: return "UIAAndUCS2";
		case OCTET6: return "OCTET6";
		case OCTET7: return "OCTET7";
		case OCTET8: return "OCTET8";
		case OCTET9: return "OCTET9";
		case OCTET10: return "OCTET10";
        default: return "?";
    }
}


