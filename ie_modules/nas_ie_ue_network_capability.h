#ifndef _UE_NETWORK_CAPABILITY_H_
#define _UE_NETWORK_CAPABILITY_H_

#include "lte_nas_ie.h"
#include "nas_ie_ue_network_capability_info_enable.h"

#define BIT_SET(v, shift) ( v |= 1UL << shift)
#define BIT_UNSET(v, shift) ( v &= 1UL << shift)

#if __BYTE_ORDER == __BIG_ENDIAN
#define BIT_TEST(v, bit)  (v & (1UL << bit) ? 1 : 0)
#else
#define BIT_TEST(v, bit)  (v & (1UL << (8 - bit - 1)) ? 1 : 0)
#endif

#define POS_LEN_COMP(len, v) do{if(len < v){return;}}while(0)

#define UE_NETWORK_CAPABILITY_SHOW_DETAILS

typedef unsigned char uint8_t;

typedef enum lte_nas_ue_network_capability_info_e{
    EEA,
    EIA,
    UEA,
    UIAAndUCS2,
    OCTET6,
    OCTET7,
    OCTET8,
    OCTET9,
    OCTET10,
}lte_nas_ue_network_capability_info_t;

//EPS encryption algorithms
enum{
	EPS_ENCRYPTION_ALG_EEA7,
	EPS_ENCRYPTION_ALG_EEA6,
	EPS_ENCRYPTION_ALG_EEA5,
	EPS_ENCRYPTION_ALG_EEA4,
	EPS_ENCRYPTION_ALG_128EEA3,
	EPS_ENCRYPTION_ALG_128EEA2,
	EPS_ENCRYPTION_ALG_128EEA1,
	EPS_ENCRYPTION_ALG_EEA0,	
};

static void nasEEA2Str(uint8_t octet)
{
	printf("        --EPS encryption algorithms:\n");
	
	printf("        	--EPS encryption algorithms EEA0 %s\n", 
				BIT_TEST(octet, EPS_ENCRYPTION_ALG_EEA0) ? "support" : "not support");
	printf("        	--EPS encryption algorithms 128-EEA1 %s\n", 
				BIT_TEST(octet, EPS_ENCRYPTION_ALG_128EEA1) ? "support" : "not support");
	printf("        	--EPS encryption algorithms 128-EEA2 %s\n", 
				BIT_TEST(octet, EPS_ENCRYPTION_ALG_128EEA2) ? "support" : "not support");
	printf("        	--EPS encryption algorithms 128-EEA3 %s\n", 
				BIT_TEST(octet, EPS_ENCRYPTION_ALG_128EEA3) ? "support" : "not support");
	printf("        	--EPS encryption algorithms EEA4 %s\n", 
				BIT_TEST(octet, EPS_ENCRYPTION_ALG_EEA4) ? "support" : "not support");
	printf("        	--EPS encryption algorithms EEA5 %s\n", 
				BIT_TEST(octet, EPS_ENCRYPTION_ALG_EEA5) ? "support" : "not support");
	printf("        	--EPS encryption algorithms EEA6 %s\n", 
				BIT_TEST(octet, EPS_ENCRYPTION_ALG_EEA6) ? "support" : "not support");
	printf("        	--EPS encryption algorithms EEA7 %s\n", 
				BIT_TEST(octet, EPS_ENCRYPTION_ALG_EEA7) ? "support" : "not support");
}

//EPS integrity algorithms
enum{
	EPS_INTEGRITY_ALG_EEA7,
	EPS_INTEGRITY_ALG_EEA6,
	EPS_INTEGRITY_ALG_EEA5,
	EPS_INTEGRITY_ALG_EEA4,
	EPS_INTEGRITY_ALG_128EEA3,
	EPS_INTEGRITY_ALG_128EEA2,
	EPS_INTEGRITY_ALG_128EEA1,
	EPS_INTEGRITY_ALG_EIA0,	
};

static void nasEIA2Str(uint8_t octet)
{
	printf("        --EPS integrity algorithms:\n");
	
	printf("        	--EPS integrity algorithms EIA0 %s\n", 
				BIT_TEST(octet, EPS_INTEGRITY_ALG_EIA0) ? "support" : "not support");
	printf("        	--EPS integrity algorithms 128-EEA1 %s\n", 
				BIT_TEST(octet, EPS_INTEGRITY_ALG_128EEA1) ? "support" : "not support");
	printf("        	--EPS integrity algorithms 128-EEA2 %s\n", 
				BIT_TEST(octet, EPS_INTEGRITY_ALG_128EEA2) ? "support" : "not support");
	printf("        	--EPS integrity algorithms 128-EEA3 %s\n", 
				BIT_TEST(octet, EPS_INTEGRITY_ALG_128EEA3) ? "support" : "not support");
	printf("        	--EPS integrity algorithms EEA4 %s\n", 
				BIT_TEST(octet, EPS_INTEGRITY_ALG_EEA4) ? "support" : "not support");
	printf("        	--EPS integrity algorithms EEA5 %s\n", 
				BIT_TEST(octet, EPS_INTEGRITY_ALG_EEA5) ? "support" : "not support");
	printf("        	--EPS integrity algorithms EEA6 %s\n", 
				BIT_TEST(octet, EPS_ENCRYPTION_ALG_EEA6) ? "support" : "not support");
	printf("        	--EPS integrity algorithms EEA7 %s\n", 
				BIT_TEST(octet, EPS_INTEGRITY_ALG_EEA7) ? "support" : "not support");
}

//UMTS encryption algorithms
enum{
	UMTS_ENCRYPTION_ALG_UEA7,
	UMTS_ENCRYPTION_ALG_UEA6,
	UMTS_ENCRYPTION_ALG_UEA5,
	UMTS_ENCRYPTION_ALG_UEA4,
	UMTS_ENCRYPTION_ALG_UEA3,
	UMTS_ENCRYPTION_ALG_UEA2,
	UMTS_ENCRYPTION_ALG_UEA1,
	UMTS_ENCRYPTION_ALG_UEA0,	
};

static void nasUEA2Str(uint8_t octet)
{
	printf("	--UMTS encryption algorithms:\n");
	
	printf("		--UMTS integrity algorithms UEA0 %s\n", 
				BIT_TEST(octet, UMTS_ENCRYPTION_ALG_UEA0) ? "support" : "not support");
	printf("		--UMTS encryption algorithms UEA1 %s\n", 
				BIT_TEST(octet, UMTS_ENCRYPTION_ALG_UEA1) ? "support" : "not support");
	printf("		--UMTS encryption algorithms UEA2 %s\n", 
				BIT_TEST(octet, UMTS_ENCRYPTION_ALG_UEA2) ? "support" : "not support");
	printf("		--UMTS encryption algorithms UEA3 %s\n", 
				BIT_TEST(octet, UMTS_ENCRYPTION_ALG_UEA3) ? "support" : "not support");
	printf("		--UMTS encryption algorithms UEA4 %s\n", 
				BIT_TEST(octet, UMTS_ENCRYPTION_ALG_UEA4) ? "support" : "not support");
	printf("		--UMTS encryption algorithms UEA5 %s\n", 
				BIT_TEST(octet, UMTS_ENCRYPTION_ALG_UEA5) ? "support" : "not support");
	printf("		--UMTS encryption algorithms UEA6 %s\n", 
				BIT_TEST(octet, UMTS_ENCRYPTION_ALG_UEA6) ? "support" : "not support");
	printf("		--UMTS encryption algorithms UEA7 %s\n", 
				BIT_TEST(octet, UMTS_ENCRYPTION_ALG_UEA7) ? "support" : "not support");
}	

//Octet 6
enum{
	/*bit 1-7 : UMTS integrity algorithms*/
	UMTS_INTEGRITY_ALG_UIA7,
	UMTS_INTEGRITY_ALG_UIA6,
	UMTS_INTEGRITY_ALG_UIA5,
	UMTS_INTEGRITY_ALG_UIA4,
	UMTS_INTEGRITY_ALG_UIA3,
	UMTS_INTEGRITY_ALG_UIA2,
	UMTS_INTEGRITY_ALG_UIA1,
};

static void nasUIAandUCS2ToStr(uint8_t octet)
{
	printf("	--UMTS integrity algorithms:\n");
	
	printf("        	--UMTS integrity algorithms UIA1 %s\n", 
				BIT_TEST(octet, UMTS_INTEGRITY_ALG_UIA1) ? "support" : "not support");
	printf("        	--UMTS integrity algorithms UIA2 %s\n", 
				BIT_TEST(octet, UMTS_INTEGRITY_ALG_UIA2) ? "support" : "not support");
	printf("        	--UMTS integrity algorithms UIA3 %s\n", 
				BIT_TEST(octet, UMTS_INTEGRITY_ALG_UIA3) ? "support" : "not support");
	printf("        	--UMTS integrity algorithms UIA4 %s\n", 
				BIT_TEST(octet, UMTS_INTEGRITY_ALG_UIA4) ? "support" : "not support");
	printf("        	--UMTS integrity algorithms UIA5 %s\n", 
				BIT_TEST(octet, UMTS_INTEGRITY_ALG_UIA5) ? "support" : "not support");
	printf("        	--UMTS integrity algorithms UIA6 %s\n", 
				BIT_TEST(octet, UMTS_INTEGRITY_ALG_UIA6) ? "support" : "not support");
	printf("        	--UMTS integrity algorithms UIA7 %s\n", 
				BIT_TEST(octet, UMTS_INTEGRITY_ALG_UIA7) ? "support" : "not support");

	//octet bit8 is for UCS2
	printf("	--UCS2 %s\n", 
				BIT_TEST(octet, 7) ? "support" : "not support");
	
}

//octet 7
enum{
	UE_CAP_OCTET7_BIT1_NF,
	UE_CAP_OCTET7_BIT2_1XSRVCC,
	UE_CAP_OCTET7_BIT3_LCS,
	UE_CAP_OCTET7_BIT4_LPP,
	UE_CAP_OCTET7_BIT5_ACC_CSFB,
	UE_CAP_OCTET7_BIT6_ASH,
	UE_CAP_OCTET7_BIT7_PROSE,
	UE_CAP_OCTET7_BIT8_PROSE_DD,
};

static void nasOctet7ToStr(uint8_t octet)
{
	printf("	--notification procedure %s\n",
				BIT_TEST(octet, UE_CAP_OCTET7_BIT1_NF) ? "support" : "not support");
	printf("	--SRVCC from E-UTRAN to cdma2000® 1x CS %s\n",
				BIT_TEST(octet, UE_CAP_OCTET7_BIT2_1XSRVCC) ? "support" : "not support");
	printf("	--LCS notification mechanisms %s\n",
				BIT_TEST(octet, UE_CAP_OCTET7_BIT3_LCS) ? "support" : "not support");
	printf("	--LTE Positioning Protocol (LPP) %s\n",
				BIT_TEST(octet, UE_CAP_OCTET7_BIT4_LPP) ? "support" : "not support");
	printf("	--eNodeB-based access class control for CSFB %s\n",
				BIT_TEST(octet, UE_CAP_OCTET7_BIT5_ACC_CSFB) ? "support" : "not support");
	printf("	--H.245 after SRVCC handover capability %s\n",
				BIT_TEST(octet, UE_CAP_OCTET7_BIT6_ASH) ? "support" : "not support");
	printf("	--ProSe capability %s\n",
				BIT_TEST(octet, UE_CAP_OCTET7_BIT7_PROSE) ? "support" : "not support");
	printf("	--ProSe direct discovery capability %s\n",
				BIT_TEST(octet, UE_CAP_OCTET7_BIT8_PROSE_DD) ? "support" : "not support");
}


//octet 8
enum{
	UE_CAP_OCTET8_BIT1_PROSE_DC,
	UE_CAP_OCTET8_BIT2_PROSE_RELAY,
	UE_CAP_OCTET8_BIT3_CP_CIOT,
	UE_CAP_OCTET8_BIT4_UP_CIOT,
	UE_CAP_OCTET8_BIT5_S1U_DATA,
	UE_CAP_OCTET8_BIT6_ERWO_PDN,
	UE_CAP_OCTET8_BIT7_HCCP_CIOT,
	UE_CAP_OCTET8_BIT8_EPCO,
};

static void nasOctet8ToStr(uint8_t octet)
{
	printf("	--ProSe direct communication %s\n",
				BIT_TEST(octet, UE_CAP_OCTET8_BIT1_PROSE_DC) ? "support" : "not support");
	printf("	--ProSe UE-to-network-relay %s\n",
				BIT_TEST(octet, UE_CAP_OCTET8_BIT2_PROSE_RELAY) ? "support" : "not support");
	printf("	--Control plane CIoT EPS optimization %s\n",
				BIT_TEST(octet, UE_CAP_OCTET8_BIT3_CP_CIOT) ? "support" : "not support");
	printf("	--User plane CIoT EPS optimization %s\n",
				BIT_TEST(octet, UE_CAP_OCTET8_BIT4_UP_CIOT) ? "support" : "not support");
	printf("	--S1-u data transfer %s\n",
				BIT_TEST(octet, UE_CAP_OCTET8_BIT5_S1U_DATA) ? "support" : "not support");
	printf("	--EMM-REGISTERED without PDN connection %s\n",
				BIT_TEST(octet, UE_CAP_OCTET8_BIT6_ERWO_PDN) ? "support" : "not support");
	printf("	--Header compression for control plane CIoT EPS optimization %s\n",
				BIT_TEST(octet, UE_CAP_OCTET8_BIT7_HCCP_CIOT) ? "support" : "not support");
	printf("	--Extended protocol configuration options %s\n",
				BIT_TEST(octet, UE_CAP_OCTET8_BIT8_EPCO) ? "support" : "not support");
}

enum{
	UE_CAP_OCTET9_BIT1_DRB,
	UE_CAP_OCTET9_BIT2_PC5,
	UE_CAP_OCTET9_BIT3_RTEC,
	UE_CAP_OCTET9_BIT4_CP_BACKOFF,
	UE_CAP_OCTET9_BIT5_DCNR,
	UE_CAP_OCTET9_BIT6_N1MODE,
	UE_CAP_OCTET9_BIT7_SGC,
	UE_CAP_OCTET9_BIT8_15BEARERS,
};

static void nasOctet9ToStr(uint8_t octet)
{
	printf("	--Multiple user plane radio bearers %s\n",
				BIT_TEST(octet, UE_CAP_OCTET9_BIT1_DRB) ? "support" : "not support");
	printf("	--The capability for V2X communication over E-UTRA-PC5 %s\n",
				BIT_TEST(octet, UE_CAP_OCTET9_BIT2_PC5) ? "support" : "not support");
	printf("	--Restriction on use of enhanced coverage %s\n",
				BIT_TEST(octet, UE_CAP_OCTET9_BIT3_RTEC) ? "support" : "not support");
	printf("	--Control plane data backoff %s\n",
				BIT_TEST(octet, UE_CAP_OCTET9_BIT4_CP_BACKOFF) ? "support" : "not support");
	printf("	--Dual connectivity with NR %s\n",
				BIT_TEST(octet, UE_CAP_OCTET9_BIT5_DCNR) ? "support" : "not support");
	printf("	--N1 mode %s\n",
				BIT_TEST(octet, UE_CAP_OCTET9_BIT6_N1MODE) ? "support" : "not support");
	printf("	--Service gap control %s\n",
				BIT_TEST(octet, UE_CAP_OCTET9_BIT7_SGC) ? "support" : "not support");
	printf("	--Signalling for a maximum number of 15 EPS bearer contexts %s\n",
				BIT_TEST(octet, UE_CAP_OCTET9_BIT8_15BEARERS) ? "support" : "not support");
}


enum{
	UE_CAP_OCTET10_BIT1_RACS,
	UE_CAP_OCTET10_BIT2_WUSA,
	UE_CAP_OCTET10_BIT3_CME,
	UE_CAP_OCTET10_BIT4_UME,
	UE_CAP_OCTET10_BIT5_VNP,
};

static void nasOctet10ToStr(uint8_t octet)
{
	printf("	--Radio capability signalling optimisation %s\n",
				BIT_TEST(octet, UE_CAP_OCTET10_BIT1_RACS) ? "support" : "not support");
	printf("	--Wake-up signal (WUS) assistance %s\n",
				BIT_TEST(octet, UE_CAP_OCTET10_BIT2_WUSA) ? "support" : "not support");
	printf("	--Control plane Mobile Terminated-Early Data Transmission %s\n",
				BIT_TEST(octet, UE_CAP_OCTET10_BIT3_CME) ? "support" : "not support");
	printf("	--User plane Mobile Terminated-Early Data Transmission %s\n",
				BIT_TEST(octet, UE_CAP_OCTET10_BIT4_UME) ? "support" : "not support");
	printf("	--V2X communication over NR-PC5 %s\n",
				BIT_TEST(octet, UE_CAP_OCTET10_BIT5_VNP) ? "support" : "not support");
}


void nas_ie_ue_network_capability_parse(const char *data, unsigned int len, lte_nas_ie_info_noticer noticer, void *priv);
const char *nas_ie_ue_network_capability_info_id_to_str(unsigned int id);



#endif
