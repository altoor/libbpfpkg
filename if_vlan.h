/* SPDX-License-Identifier: GPL-2.0+ WITH Linux-syscall-note */
#ifndef _BPF_IF_VLAN_H_
#define _BPF_IF_VLAN_H_

#include <linux/if_ether.h>

/*
 *	IEEE 802.1Q/802.3ac magic constants. The frame sizes omit the preamble
 *	and FCS/CRC (frame check sequence).
 */
#define VLAN_HLEN	4		/* The additional bytes required by VLAN
					 * (in addition to the Ethernet header)
					 */
#define VLAN_ETH_HLEN	18		/* Total octets in header.	 */
#define VLAN_ETH_ZLEN	64		/* Min. octets in frame sans FCS */
#define VLAN_ETH_DATA_LEN	1500	/* Max. octets in payload	 */
#define VLAN_ETH_FRAME_LEN	1518	/* Max. octets in frame sans FCS */

/*
 * This is an 802.1Q (VLAN) header.
 */
struct vlan_hdr {
	__be16	h_vlan_TCI;
	__be16	h_vlan_encapsulated_proto;
};

/*
 * This is a full Ethernet/802.1Q frame header
 */
struct vlan_ethhdr {
	unsigned char	h_dest[ETH_ALEN];
	unsigned char	h_source[ETH_ALEN];
	__be16		h_vlan_proto;
	__be16		h_vlan_TCI;
	__be16		h_vlan_encapsulated_proto;
};

#define VLAN_PRIO_MASK		0xe000 /* Priority Code Point */
#define VLAN_PRIO_SHIFT		13
#define VLAN_CFI_MASK		0x1000 /* Canonical Format Indicator /
					* Drop Eligible Indicator */
#define VLAN_VID_MASK		0x0fff /* VLAN Identifier */
#define VLAN_N_VID		4096

#endif /* !(_BPF_IF_VLAN_H_) */
