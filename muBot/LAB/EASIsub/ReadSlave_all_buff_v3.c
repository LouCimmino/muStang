#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>
#include <fcntl.h>
#include <time.h>
#include <sys/mman.h>
#include <unistd.h>
#include <sys/time.h>
#include <sys/timeb.h>
#include <pthread.h>
#include "map.h"
#define PAGE_SIZE (4*1024)
#define BLOCK_SIZE (4*1024)

int  mem_fd;
void *gpio_map;
#define BCM2708_PERI_BASE        0x20000000
#define GPIO_BASE                (BCM2708_PERI_BASE + 0x200000)

volatile unsigned *gpio;

#define INP_GPIO(g) *(gpio+((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g) *(gpio+((g)/10)) |=  (1<<(((g)%10)*3))
#define SET_GPIO_ALT(g,a) *(gpio+(((g)/10))) |= (((a)<=3?(a)+4:(a)==4?3:2)<<(((g)%10)*3))

#define GPIO_LEV *(gpio+13)

#define GPIO_SET *(gpio+7)
#define GPIO_CLR *(gpio+10)

struct arg {
    unsigned int *buffer;
    long long int *tss;
    int *trg;
    int size_buffer;
    int n;
};
typedef struct arg arg;

void reset();
void setup_io();
void ciclo_clock();
void delay_clock(int delay);
void set_pin_output(unsigned short pin);
unsigned int read_easy(void);
unsigned int trig(unsigned short pin);
void send_word(int GPIOpin, unsigned short word_to_send);
void* fileDownload(void *ptr);

int mtime_stamp(){
	struct timeb timer_msec;
	long long int timestamp_msec; /* timestamp in millisecond. */
	if (!ftime(&timer_msec)) {
		timestamp_msec = ((long long int) timer_msec.time) * 1000ll + (long long int) timer_msec.millitm;
	}
	else {
		timestamp_msec = -1;
	}
	printf("%lld (msec)\n", timestamp_msec);
}

long long int mtime_stamp_d(){
	struct timeb timer_msec_d;
	long long int timestamp_msec_d; /* timestamp in millisecond. */
	if (!ftime(&timer_msec_d)) {
		timestamp_msec_d = ((long long int) timer_msec_d.time) * 1000ll + (long long int) timer_msec_d.millitm;
	}
	else {
		timestamp_msec_d = -1;
	}
	return(timestamp_msec_d);
}


static volatile int thrdTot = 10;
pthread_t tid;

FILE *f;

int main (int argc, char *argv[])
{
	printf(" START: ");
	mtime_stamp();
	int addr;
	int num_evt;
	int pktCount;
	int Npato;
	int trgArr[12];
	int flineArr[12]; 
	int addrArr[12];
	setup_io();
	set_pin_output(DLAY_CLK);
	set_pin_output(READ_PIN);
	set_pin_output(DTK);
	set_pin_output(CLK);
	set_pin_output(CHPSEL);
	set_pin_output(MOSI);
	set_pin_output(START_FIFO);
	set_pin_output(RST);
	INP_GPIO(MISO);
	
	int gotOne22, gotOne24, pin, i, k, ii;
	unsigned long int kk;
	int myCounter22, myCounter24, size_buff, size_buff_tss;
	int err[thrdTot];
	int tr = 0;
	
	unsigned int *temp;
	long long int *temp_tss;
	unsigned int **buff = (unsigned int **) malloc(thrdTot *sizeof(unsigned int));
	long long int buff_tss[20000];
	int buff_trg[240000];
	kk = 0;
	k = 0;
	size_buff = 0;
	size_buff_tss = 0;
	buff[tr] = (unsigned int*) malloc(sizeof(unsigned int));
	num_evt = (int)strtol(argv[1], NULL, 10);

	for (;;) {
		GPIO_CLR = 1 << READ_PIN;
		GPIO_CLR = 1 << CHPSEL;
		send_word(MOSI, CMD_CLR);
		send_word(MOSI, CMD_CTRLWD);
		send_word(MOSI, CMD_RUN);
		GPIO_SET =1 <<CHPSEL;
		GPIO_SET =1 <<READ_PIN;

		gotOne22 = 0 ;
		for (;;) {
			if (trig(TRG_IRQ) == 1) {
				GPIO_CLR = 1 << READ_PIN;
				GPIO_CLR = 1 << CHPSEL;
				send_word(MOSI, CMD_CTRLWD);
				send_word(MOSI, CMD_DIAG);
				GPIO_SET =1 <<CHPSEL;
				GPIO_SET =1 <<READ_PIN;
//----------------------------
				delay_clock(600);

				for (ii=2; ii<argc; ii++) {
					pktCount = 0;
					addr = (int)strtol(argv[ii], NULL, 10);
					GPIO_CLR = 1 << READ_PIN;
					GPIO_CLR = 1 << CHPSEL;
					send_word(MOSI, CMD_EASY);
					send_word(MOSI, CMD_READ | (addr << 10));
					GPIO_SET =1 <<CHPSEL;
					GPIO_SET =1 <<READ_PIN;

					GPIO_SET = 1 << START_FIFO;
					GPIO_SET = 1 << START_FIFO;
					GPIO_SET = 1 << START_FIFO;
					GPIO_CLR = 1 << START_FIFO;
					GPIO_CLR = 1 << START_FIFO;

					gotOne24 = 0;
					for (;;) {
						if (trig(FIFO_READY) == 1) {
							buff[tr][size_buff]=read_easy();
							++gotOne24;
							++pktCount;
							temp = realloc(buff[tr], (size_buff+2)*sizeof(unsigned int));
							if (temp != NULL) {
								buff[tr] = temp;
								++size_buff;
							}

						}
						if (gotOne24 != 0)
							break ;
					}
					gotOne24 = 0;
					for (;;) {
						buff[tr][size_buff]=read_easy();
						++pktCount;
						//if ((pktCount == 40) && (trig(FIFO_READY) == 1)) {
						//	GPIO_CLR = 1 << READ_PIN;
						//	GPIO_CLR = 1 << CHPSEL;
						//	send_word(MOSI, CMD_RSTFIFO);
						//	GPIO_SET =1 <<CHPSEL;
						//	GPIO_SET =1 <<READ_PIN;
						//	printf("---> MORE THAN 40 PCK\n");
						//	break;
						//}
						temp = realloc(buff[tr], (size_buff+2)*sizeof(unsigned int));
						if (temp != NULL) {
							buff[tr] = temp;
							++size_buff;
						}
						if (trig(FIFO_READY) == 0)
							++gotOne24;
						if (gotOne24 != 0)
							break ;
					}
					if (pktCount >= 39) {
						buff_trg[k] = kk;
						k++;
					}
				}
				++gotOne22;
				kk++;
				buff_tss[size_buff_tss] = mtime_stamp_d();
			}
			if (gotOne22 != 0)
				break ;
		}
		++size_buff_tss;
		if (kk >= num_evt)
			break;

	}
	printf("  STOP: ");
	mtime_stamp();
	fileDownload( &(arg){buff[tr], buff_tss, buff_trg, size_buff-1, 1});
	pthread_exit(NULL);
	return 0 ;
	
}

void set_pin_output(unsigned short pin)
{
  INP_GPIO(pin);
  OUT_GPIO(pin);
}

unsigned int read_easy()
{
  int i;
  unsigned int buffer=0;
  unsigned int value;
  unsigned char pin_value ;

  
  GPIO_SET = 1 << DTK;
  GPIO_SET = 1 << DTK;
  GPIO_SET = 1 << DTK;
  GPIO_SET = 1 << DTK;
  GPIO_CLR = 1 << DTK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_CLR = 1 << CLK;
  for (i = 30; i>=0; i--)
    {
	value = GPIO_LEV;               // reading all 32 pins
	pin_value = ((value & (1 << MISO)) != 0); // get pin MISO value 
	buffer|=((pin_value&1)<<i);
	ciclo_clock();
    }
  return(buffer);
}


void setup_io()
{
   if ((mem_fd = open("/dev/mem", O_RDWR|O_SYNC) ) < 0) {
      printf("Error no /dev/mem \n");
      exit(-1);
   }

   /* mmap GPIO */
   gpio_map = mmap(
      NULL,             //Any adddress in our space will do
      BLOCK_SIZE,       //Map length
      PROT_READ|PROT_WRITE,// Enable reading & writting to mapped memory
      MAP_SHARED,       //Shared with other processes
      mem_fd,           //File to map
      GPIO_BASE         //Offset to GPIO peripheral
   );

   close(mem_fd);

   if (gpio_map == MAP_FAILED) {
      printf("mmap error %d\n", (int)gpio_map);//errno also set!
      exit(-1);
   }
   gpio = (volatile unsigned *)gpio_map;
}

void ciclo_clock() {
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_SET = 1 << CLK;
  GPIO_CLR = 1 << CLK;
  GPIO_CLR = 1 << CLK;
}

void send_word(int GPIOpin, unsigned short word_to_send) {

	int bit[16];
	int i = 0;
	int modulo;
	int quoziente;
	
	for (i=0; i<16; i++)
		bit[15-i] = ((word_to_send & 1<<i)>>i);

	GPIO_CLR = 1<<GPIOpin; //DOpening

	for (i=0; i<16; i++) {
		switch (bit[i]) {
			case 0:
				GPIO_CLR = 1<<GPIOpin;
				break;
			default :
				GPIO_SET = 1<<GPIOpin;
				break;
		}
		ciclo_clock();
	}

	GPIO_CLR = 1<<GPIOpin; //DClosure
}

void delay_clock(int delay) {
	int j;
	for (j = 0; j < delay; j++) {
		GPIO_SET = 1<<DLAY_CLK;
		GPIO_CLR = 1<<DLAY_CLK;
	}

}

unsigned int trig(unsigned short pin)
{
  unsigned int value;
  unsigned char pin_value ;

  INP_GPIO(pin);
    
  value = GPIO_LEV;               // reading all 32 pins
  pin_value = ((value & (1 << pin)) != 0); // get pin MISO value 
  return(pin_value);
}

void* fileDownload(void *ptr)
{
	pthread_t id = pthread_self();
	
	char name[20];
	int i = 0;
	int j = 1;
	int k = 1;
	int l = 0;
	int ck = 0;
	arg *x = ptr;
	
	sprintf(name, "/home/DatiTB/slaveData");
	
	f = fopen(name, "a+");

	while (i <= x->size_buffer) {
		while (ck == 0) {
			if ((x->buffer[i] == 0x25555) && (x->buffer[i+1] == 0x0) && (i != x->size_buffer)) {
				i = i+2;
			}
			else ck = 1;
		}
		ck = 0;
		fprintf(f, "%x\t", x->buffer[i]);
		++i;
		++j;
		++k;
		if (j == 40) { 
			fprintf(f, "%lld\n", x->tss[x->trg[l]]);
			j = 1;
			l++;
		}
		if (k == 469) {
			k = 1;
		}
	}
	fclose(f);
	return NULL;
}
