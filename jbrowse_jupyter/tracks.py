import re
# elif protocol == "localPath":
# return { "uri": location, "locationType": "LocalPathLocation"}
def make_location(location, protocol):
    if protocol == "uri":
        return { "uri": location, "locationType": "UriLocation"}
    else:
        raise TypeError(f"invalid protocol {protocol}")

def supported_track_type(trackType):
    return trackType in {'AlignmentsTrack', 'QuantitativeTrack', 'VariantTrack', 'FeatureTrack'}

def guess_track_type(adapterType):
  known =  {
    "BamAdapter": "AlignmentsTrack",
    "CramAdapter": "AlignmentsTrack",
    "BgzipFastaAdapter": "ReferenceSequenceTrack",
    "BigWigAdapter": "QuantitativeTrack",
    "IndexedFastaAdapter": "ReferenceSequenceTrack",
    "TwoBitAdapter": "ReferenceSequenceTrack",
    "VcfTabixAdapter": "VariantTrack",
    "HicAdapter": "HicTrack",
    "PAFAdapter": "SyntenyTrack",
  }
  if adapterType in known:
    return known[adapterType]
  else:
    return "FeatureTrack"

  

def guess_adapter_type(fileName, protocol, index="defaultIndex"):
  # file types
  bam = re.compile(r'\.bam$', re.IGNORECASE)
  bed = re.compile(r'\.bed$',re.IGNORECASE)
  bedTabix = re.compile(r'\.bed\.b?gz$',re.IGNORECASE)
  bigBed = re.compile(r'\.(bb|bigbed)$',re.IGNORECASE)
  bigWig = re.compile(r'\.(bw|bigwig)$',re.IGNORECASE)
  cram = re.compile(r'\.cram$', re.IGNORECASE)
  fastaidx = re.compile(r'\.(fa|fasta|fna|mfa)$', re.IGNORECASE)
  fastaGz = re.compile(r'\.(fa|fasta|fna|mfa)\.b?gz$', re.IGNORECASE)
  gff3 = re.compile(r'\.gff3$', re.IGNORECASE) 
  gff3Tabix = re.compile(r'\.gff3?\.b?gz$', re.IGNORECASE) 
  gtf = re.compile(r'\.gtf$', re.IGNORECASE) 
  hic = re.compile(r'\.hic', re.IGNORECASE)
  ncList = re.compile(r'\/trackData.jsonz?$', re.IGNORECASE)
  paf = re.compile(r'\.paf', re.IGNORECASE)
  sizes =re.compile(r'\.sizes$', re.IGNORECASE)
  sparql =re.compile(r'\/sparql$', re.IGNORECASE)
  twoBit =re.compile(r'\.2bit$', re.IGNORECASE)
  vcf = re.compile(r'\.vcf$', re.IGNORECASE)
  vcfGzp = re.compile(r'\.vcf\.b?gz$', re.IGNORECASE)
  vcfIdx = re.compile(r'\.vcf\.idx$', re.IGNORECASE)

  # bam
  if bool(re.search(bam, fileName)): 
    return {
      "type": "BamAdapter",
      "bamLocation": make_location(fileName, protocol),
      "index": {
        "location": make_location(index or f'{fileName}.bai', protocol),
        "indexType": 'CSI' if (index != "defaultIndex" and index.upper().endswith("CSI")) else "BAI",
      },
    }
  # cram
  if bool(re.search(cram, fileName)): 
      return {
        "type": 'CramAdapter',
        "cramLocation": make_location(fileName, protocol),
        "craiLocation": make_location(f'{fileName}.crai', protocol),
      }
    
  # gff3
  if bool(re.search(gff3, fileName)):
    return {
        "type": 'UNSUPPORTED',
    }

  # gtf
  if bool(re.search(gtf, fileName)):
    return {
        "type": 'UNSUPPORTED',
    }

  # gff3 tabix
  if bool(re.search(gff3Tabix, fileName)): 
    return {
      "type": "Gff3TabixAdapter",
      "gffGzLocation": make_location(fileName, protocol),
      "index": {
        "location": make_location(f'{fileName}.tbi', protocol),
        "indexType": "TBI",
      },
    }
    
  # vcf
  if bool(re.search(vcf, fileName)):
    return {
      "type": "VcfAdapter",
      "vcfLocation": make_location(fileName, protocol),
    }

  # vcf idx
  if bool(re.search(vcfIdx, fileName)):
    return {
        "type": 'UNSUPPORTED',
    }
   
  # vcf gzipped
  if bool(re.search(vcfGzp, fileName)):
    return {
      "type": "VcfTabixAdapter",
      "vcfGzLocation": make_location(fileName, protocol),
      "index": {
        "location": make_location(f'{fileName}.tbi', protocol),
        "indexType": "CSI" if (index != "defaultIndex" and index.upper().endswith("CSI")) else "TBI",
      },
    }
  
  # bigwig
  if bool(re.search(bigWig, fileName)):
    return {
      "type": "BigWigAdapter",
      "bigWigLocation": make_location(fileName, protocol),
    }
  # bed
  if bool(re.search(bed, fileName)):
    return {
        "type": 'UNSUPPORTED',
    }
  
  # bed gz
  if bool(re.search(bedTabix, fileName)):
    return {
      "type": "BedTabixAdapter",
      "bedGzLocation": make_location(fileName, protocol),
      "index": {
        "location": make_location(f'{fileName}.tbi', protocol),
        "indexType": "CSI" if (index != "defaultIndex" and index.upper().endswith("CSI")) else "TBI",
      },
    }

  # bigbed
  if bool(re.search(bigBed, fileName)):
    return {
      "type": "BigBedAdapter",
      "bigBedLocation": make_location(fileName, protocol),
    }
  
  # fasta indexed
  if bool(re.search(fastaidx, fileName)):
    return {
      "type": "IndexedFastaAdapter",
      "fastaLocation": make_location(fileName, protocol),
      "faiLocation": makeLocation(f'{fileName}.fai', protocol)
    }

  # Bgzipped fasta 
  if bool(re.search(fastaGz, fileName)):
    return {
      "type": "IndexedFastaAdapter",
      "fastaLocation": make_location(fileName, protocol),
      "faiLocation": makeLocation(f'{fileName}.fai', protocol),
      "gziLocation": makeLocation(f'{fileName}.gzi', protocol)
    }

  # twobit
  if bool(re.search(twoBit, fileName)):
    return {
      "type": "TwoBitAdapter",
      "twoBitLocation": make_location(fileName, protocol),
    }
  # sizes
  if bool(re.search(twoBit, fileName)):
    return {
        "type": 'UNSUPPORTED',
    }
  # nclist
  if bool(re.search(ncList, fileName)):
    return {
      "type": "NCListAdapter",
      "rootUrlTemplate": make_location(fileName, protocol),
    }
  
  # SPARQL
  if bool(re.search(sparql, fileName)):
    return {
      "type": "SPARQLAdapter",
      "endpoint": make_location(fileName, protocol),
    }
  
  # hic
  if bool(re.search(hic, fileName)):
    return {
      "type": "HicAdapter",
      "hicLocation": make_location(fileName, protocol),
    }
  
  # paf
  if bool(re.search(paf, fileName)):
    return {
      "type": "PAFAdapter",
      "pafLocation": make_location(fileName, protocol),
    }
  
  return {
    "type": 'UNKNOWN',
  }

