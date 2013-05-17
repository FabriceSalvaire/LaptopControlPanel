/****************************************************************************************************
 *
 * Copyright (C) 2012 Fabrice Salvaire.  All Rights Reserved.
 *
 ***************************************************************************************************/

/* *********************************************************************************************** */

/*
 * Some of these snippets comes from OpenCV-2.3.x/modules/core/src/system.cpp
 *
 */

/* *********************************************************************************************** */

#include <stdlib.h>
#include <unistd.h>

#include "IntelCpuTools.hpp"

/* *********************************************************************************************** */

extern "C" {
//! Number of CPUs
/**
 *  \return the number of cpus
 */
size_t number_of_cores()
{
#if defined WIN32 || defined _WIN32
  SYSTEM_INFO sysinfo;
  GetSystemInfo(&sysinfo);
  return (int)sysinfo.dwNumberOfProcessors;

#elif defined __linux__
  return (size_t) sysconf(_SC_NPROCESSORS_ONLN);
#endif
}
}

/* *********************************************************************************************** */

extern "C" {
//! Read CPUID 
/**
 *  \param cpuid function
 *
 *  \return eax, ebx, ecx, edx registers
 */
void
read_cpuid(size_t function, size_t &eax, size_t &ebx, size_t &ecx, size_t &edx)
{
  // #if defined __GNUC__ && defined __x86_64__
  __asm__ __volatile__
    (
     "movl %[function], %%eax\n\t"
     "cpuid\n\t"
     : "=a" (eax), "=b" (ebx), "=c" (ecx), "=d" (edx)
     : [function] "m" (function) 
     : "cc"
     );
}
}

/* *********************************************************************************************** */

CpuFeatures::CpuFeatures()
  : has()
{
  size_t eax, ebx, ecx, edx;
  const size_t FEATURE_INFORMATION = 0x1;

  read_cpuid(FEATURE_INFORMATION, eax, ebx, ecx, edx);
  size_t family = mask_field(eax, 8, 11);
  if (family >= 6)
    {
      // Feature Flags Reported in the ECX Register
      has[SSE3] = test_bit(ecx, 0);
      has[PCLMULDQ] = test_bit(ecx, 1);
      has[SSSE3] = test_bit(ecx, 9);
      has[FMA] = test_bit(ecx, 12);
      has[SSE4_1] = test_bit(ecx, 19);
      has[SSE4_2] = test_bit(ecx, 20);
      has[POPCNT] = test_bit(ecx, 23);
      has[AVX] = test_bit(ecx, 28);

      // Feature Flags Reported in the EDX Register
      has[MMX] = test_bit(edx, 23);
      has[SSE] = test_bit(edx, 25);
      has[SSE2] = test_bit(edx, 26);
    }
}

size_t
CpuFeatures::mask_field(size_t cpuid_data, size_t start_bit, size_t stop_bit)
{
  size_t number_of_bits = stop_bit - start_bit +1;
  size_t mask = (1 << number_of_bits) -1;
  return (cpuid_data >> start_bit) & mask;
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
