import re

def make_location(location, protocol):
    if protocol == "uri":
        return { "uri": location, "locationType": "UriLocation"}
    elif protocol == "localPath":
        return { "uri": location, "locationType": "LocalPathLocation"}
    else:
        raise TypeError(f"invalid protocol {protocol}")

# track_alignments(): visualize BAM or CRAM alignment data
# track_feature(): visualize GFF3 data
# track_variant(): visualize VCF data
# track_wiggle(): visualize bigWig data (quantitative is wiggle)
def guessTrackType(adapterType):
  print("adapter type in guess track", adapterType)
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

def guessAdapterType(fileName, protocol, index="defaultIndex"):
  bam = re.compile(r'\.bam$', re.IGNORECASE) 
  cram = re.compile(r'\.cram$', re.IGNORECASE)
  vcf = re.compile(r'\.vcf$', re.IGNORECASE)
  vcfGzp = re.compile(r'\.vcf\.b?gz$', re.IGNORECASE)
  gff3Tabix = re.compile(r'\.gff3?\.b?gz$', re.IGNORECASE) 
  bigWig = re.compile(r'\.(bw|bigwig)$',re.IGNORECASE )
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
  
  return {
    "type": 'UNKNOWN',
  }
    
    
def supportedTrackType(trackType):
    return trackType in {'AlignmentsTrack', 'ReferenceSequenceTrack', 'VariantTrack', 'FeatureTrack'}
