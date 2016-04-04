#!/usr/bin/env python
from __future__ import division
import sys
from Bio import SeqIO


'''
__author__: Da
Date: 21/03/2016
'''

#Support Class to create alignments and check relationships between alignments
class Alignment:
  def __init__(self, chr, pos, strand):
    self.chr = str(chr)
    self.pos = str(pos)
    self.strand = str(strand)

  def is_concordant_with(self, other):
    return False

  def __repr__(self):
	return self.chr+" "+str(self.pos)+" "+self.strand
  # for comparison

  def __cmp__(self, other):
        if int(self.pos) == int(other.pos):
            return 0
        elif int(self.pos) > int(other.pos):
            return 1
        else: return -1

#Support class to execute the handiwork of read alignment to a reference sequence
class Aligner1:
  def __init__(self, ref):
    self.refname = ref.id
    self.refseq = ref.seq
    self.rrefseq = ref.seq.reverse_complement()

  def align(self, read):
    # Providing two methods to align the gene.
    # return self.cal_naive(self.refseq, self.rrefseq, read.seq)
    return self.cal_led(self.refseq, self.rrefseq, read.seq)

  #get result by the led search
  def cal_led(self, ref, rref, read):
    alignments = []
    positive = self.led_method(ref, read)
    for p_r in positive:
      alignment = Alignment(p_r['chr'],p_r['pos'],'+')
      alignments.append(alignment)
    negtive = self.led_method(rref, read)
    for n_r in negtive:
      alignment = Alignment(n_r['chr'],len(self.refseq)-int(n_r['pos']),'-')
      alignments.append(alignment)
    alignments = sorted(alignments)
    print alignments
    return alignments

  # calculate by the local edit distance
  def led_method(self, ref, read):
    result_list = []
    F = [[0 for col in range(len(ref)+1)] for row in range(0,len(read)+1)]
    for i in range(1,len(read)+1):
      for j in range(1,len(ref)+1):
        if ref[j-1] == read[i-1]:
          var = 1
        else:
          var = -1
        F[i][j] = max(0,F[i-1][j]-1,F[i][j-1]-1,F[i-1][j-1]+var)
        if F[i][j] == len(read):
          result = dict()
          result['pos'] = str(j-len(read)+1)
          result['chr'] = str(ref[j-len(read):j])
          result_list.append(result)
    return result_list

  #get result by the navie search
  def cal_naive(self, ref, rref, read):
    alignments = []
    for x in range(0,len(ref)):
            if ref[x:x+len(read)]== read:
              # print "read_id:%s"%each_read.id
              # print "positon:%s" %x
              # print "ref>%s"%self.refseq[x:x+len(read.seq)]
              # print ""
              alignment = Alignment(self.refseq[x:x+len(read)],x+1,'+',)
              alignments.append(alignment)
            if rref[x:x+len(read)] == read:
              alignment = Alignment(self.rrefseq[x:x+len(read)],len(self.refseq)-(x+1),'-')
              alignments.append(alignment)
    alignments = sorted(alignments)
    print alignments
    return alignments


#Check the command line arguments
if __name__ == '__main__':
  # Wrong Parameter:
  if len(sys.argv) < 3:
    print "Usage: <reference file (fasta)> <read file (fasta)> "
    sys.exit(0)

  #Read the reference sequence and initiate the aligner
  try:
    for s in SeqIO.parse(sys.argv[1], "fasta"):
      f = open('alignment1.txt','w')
      aligner = Aligner1(s)
      align_0 = 0
      align_1 = 0
      align_over_2 = 0
      count_all = 0
      # get each read aligned
      for each_read in SeqIO.parse(sys.argv[2], "fasta"):
        count_all += 1
        result = aligner.align(each_read)
        if result:
          if len(result) == 1:
            align_1 += 1
          else:
            align_over_2 += 1
          print each_read.id
          f.write("ReadName: %s\t"%each_read.id)
          if result[0].strand == '-':
            # f.write("Position: %s\t"%str(len(aligner.refseq)-((int(result[0].pos))+len(each_read.seq))+2))
            f.write("PositionL %s\t"%str(int(result[0].pos)-len(each_read)+2))
          else:
            f.write("Position: %s\t"%str(result[0].pos))
          f.write("Alignment: %s\tStrand: %s\tNumber of Alignments: \t%d\n"%(str(result[0].chr),str(result[0].strand),len(result)))
        else:
          align_0 += 1
          f.write("ReadName: %s\tPosition: %s\tStrand: %s\tNumber of Alignments: %s\t\n"%(each_read.id,'0','*','0'))
      f.close()
      print '''
      Alignment Statistic:
      ----------------------
      None:        %d Per:%f
      Exactly One: %d Per:%f
      Over Two:    %d Per:%f

      '''%(align_0,align_0/count_all,align_1,align_1/count_all,align_over_2,align_over_2/count_all)
      break #Stop after the fist sequence in the reference
  except IOError as e:
    print "Could not read reference sequence file (see below)!"
    print e
    sys.exit(1)