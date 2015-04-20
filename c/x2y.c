#include <stdio.h>
#include <stdlib.h>

#define READBUF_SIZE 1024
#define TMPNAME "/tmp/x2y.tmp"

static void
proc(
    const char *name
    )
{
    FILE *fp,*outfp;
    int i;
    size_t readin;
    char readbuf[READBUF_SIZE];

    /* open input file */
    if((fp = fopen(name, "r")) == NULL){
        fprintf(stderr, "%s: error reading %s\n", NAME, name);
        perror("can't open input file");
    }
    else{
        if((outfp = fopen(TMPNAME, "w")) == NULL){
            fprintf(stderr, "%s: error creating tmp file %s\n", NAME, TMPNAME);
            perror("can't create tmp file");
        }
        else{
            while((readin = fread(readbuf, 1, READBUF_SIZE, fp)) > 0){
                for(i = 0; i < readin; i++){
                    if(readbuf[i] == FROM){
                        readbuf[i] = TO;
                    }
                }
                if(fwrite(readbuf, 1, readin, outfp) != readin){
                    fprintf(stderr, "%s: error in fwrite\n", NAME);
                }
            }
            fclose(outfp);
        }
        fclose(fp);
        if(rename(TMPNAME, name) != 0){
            fprintf(stderr, "%s: error in rename for %s\n", NAME, name);
            perror("error in rename");
        }
    }
}

int
main(
     int argc,
     char **argv
     )
{
    int i;

    if(argc < 2){
        fprintf(stderr, "%s: no input files\n", NAME);
        exit(1);
    }
    for(i = 1; i < argc; i++){
        proc(argv[i]);
    }
    exit(0);
}
