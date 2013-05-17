/****************************************************************************************************
 *
 * Copyright (C) 2012 Fabrice Salvaire.  All Rights Reserved.
 *
 ***************************************************************************************************/

/* *********************************************************************************************** */

#ifndef __IntelCpuTools_H__
#define __IntelCpuTools_H__

/* *********************************************************************************************** */

#include <stdint.h>
#include <stdlib.h>

/* *********************************************************************************************** */

/*
 * The Time Stamp Counter is invariant since Nehalem Architecture
 *
 * This can be used even your program is parallel and runs on multiple
 * cores - all TSC counters are synchronized and show the same clocks
 * as like there is the only one counter in a system.
 *
 * For the latest Nehalem processors, the time stamp counter (RDTSC)
 * does not vary with the actual operating frequency of the part. This
 * is referred to as "Invariant TSC" and described in the software
 * developers manual (SDM) section 16.11.1 (
 * http://www.intel.com/Assets/PDF/manual/253668.pdf ).
 * 
 * Unlike prior parts, Nehalem's TSC does not stop across core
 * C-states. Nehalem also implements the RDTSCP instruction which
 * returns both the TSC value and a new MSR into ECX. For a full
 * explanation of RDTSCP, please see the SDM.
 * 
 * On Nehalem, the TSC runs at a constant frequency of
 * MSR_PLATFORM_INFO[15:8] * 133.33MHz. MSR_PLATFORM_INFO[15:8] will
 * report the lower of the ratio at which the part was stamped or a
 * separate MSR to lower the ratio to provide TSC consistency across
 * multi-socket systems with parts of different frequencies.
 * 
 * Synchronization of the TSC across multiple threads/cores/packages:
 * As long as software does not write the TSC, the Nehalem TSC will
 * remain synchronized across all threads, cores and packages
 * connected to a single PCH.
 * 
 * The time-stamp counter on Nehalem is reset to zero each time the
 * processor package has RESET asserted. From that point onwards the
 * TSC will continue to tick constantly across frequency changes,
 * turbo mode and ACPI C-states. All parts that see RESET
 * synchronously will have their TSC's completely synchronized. This
 * synchronous distribution of RESET is required for all sockets
 * connected to a single PCH. For large, multi-node systems, RESET
 * might not be synchronous.
 *
 */

//! Read Time-Stamp Counter
/*!
 * \return an unsigned 64-bit integer containing the time-stamp counter.
 * 
 */
// extern
__inline__ uint64_t
read_cpu_tsc()
{
  // #if defined __GNUC__
#if defined __i386__
  uint64_t tick;
  // ax:dx <- rdtsc
  __asm__ __volatile__("rdtsc" : "=A" (tick));
  return tick;
#elif defined __amd64__
  uint64_t tick_low, tick_high;
  // a, d <- rdtsc
  //  __asm__ __volatile__("rdtsc" : "=a" (tick_low), "=d" (tick_high));
  __asm__ __volatile__("rdtscp" : "=a" (tick_low), "=d" (tick_high) :: "ecx" );
  return (tick_high << 32) | tick_low;
#endif
}

/* *********************************************************************************************** */

extern "C" {
size_t number_of_cores();
}

/* *********************************************************************************************** */

// Implement a barrier
__inline__ void
cpuid()
{
  __asm__ __volatile__("cpuid" ::: "%rax", "%rbx", "%rcx", "%rdx");
}

extern "C" {
void read_cpuid(size_t function, size_t &eax, size_t &ebx, size_t &ecx, size_t &edx);
}

/* *********************************************************************************************** */

class CpuFeatures
{
public:
  enum CPU_FEATURE
    {
      AVX,
      FMA,
      MMX,
      PCLMULDQ,
      POPCNT,
      SSE,
      SSE2,
      SSE3,
      SSE4_1,
      SSE4_2,
      SSSE3,
      MAX_FEATURE
    };

public:
  CpuFeatures();

private:
  static inline bool test_bit(size_t cpuid_data, size_t bit)
  {
    return (cpuid_data & (1 << bit)) == 0 ? false : true;
  };

  static inline size_t mask_field(size_t cpuid_data, size_t start_bit, size_t stop_bit);

public:
  bool has[MAX_FEATURE];
};

/* *********************************************************************************************** */

#endif /* __IntelCpuTools_H__ */

/* *********************************************************************************************** */
