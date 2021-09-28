#include "lte_nas_ie.h"
#include "nas_ie_tracking_area_identity.h"

struct tracking_area_identity_ie{

#if __BYTE_ORDER__==__ORDER_BIG_ENDIAN__
    unsigned char MCC_digit2:4,
                    MCC_digit1:4;
    unsigned char MNC_digit3:4,
                    MCC_digit3:4;
    unsigned char MNC_digit2:4,
                    MNC_digit1:4;
#else
    unsigned char MCC_digit1:4,
                    MCC_digit2:4;
    unsigned char MCC_digit3:4,
                    MNC_digit3:4;
    unsigned char MNC_digit1:4,
                    MNC_digit2:4;
#endif

    unsigned char TAC;
    unsigned char TAC_continued;
};

static void parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv){

    unsigned short val;
    struct tracking_area_identity_ie *ie = (struct tracking_area_identity_ie *)data;
    
#ifdef CARE_TRACKING_AREA_IDENTITY_MCC
    val = (ie->MCC_digit3 << 8) | (ie->MCC_digit2 << 4) | (ie->MCC_digit1);
    noticer((unsigned int)MCC, (unsigned char *)&val, sizeof(val), priv);
#endif

#ifdef CARE_TRACKING_AREA_IDENTITY_MNC
    val = (ie->MNC_digit3 << 8) | (ie->MNC_digit2 << 4) | (ie->MNC_digit1);
    noticer((unsigned int)MNC, (unsigned char *)&val, sizeof(val), priv);
#endif

#ifdef CARE_TRACKING_AREA_IDENTITY_TAC
    noticer((unsigned int)TAC, (unsigned char *)&(ie->TAC), 2, priv);
#endif

}

void nas_ie_tracking_area_identity_parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv){
    parse(data, len, noticer, priv);
}

const char *nas_ie_tracking_area_identity_info_id_to_str(unsigned int id){
    switch(id){
        case MCC: return "MCC";
        case MNC: return "MNC";
        case TAC: return "TAI";
        default: return "?";
    }
}
