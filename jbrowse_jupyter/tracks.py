import re
import uuid
import pandas as pd
import os


# elif protocol == "localPath":
# return { "uri": location, "locationType": "LocalPathLocation"}
def make_location(location, protocol):
    if protocol == "uri":
        return { "uri": location, "locationType": "UriLocation"}
    else:
        raise TypeError(f"invalid protocol {protocol}")

def supported_track_type(trackType):
    return trackType in {'AlignmentsTrack', 'QuantitativeTrack', 'VariantTrack', 'FeatureTrack'}

def guess_display_type(trackType):
  displays = {
    "AlignmentsTrack": "LinearAlignmentsDisplay",
    "VariantTrack": "LinearVariantDisplay",
    "ReferenceSequenceTrack": "LinearReferenceSequenceDisplay",
    "QuantitativeTrack": "LinearBasicDisplay",
    "FeatureTrack": "LinearBasicDisplay"
  }
  if trackType in displays:
    return displays[trackType]
  else:
    return "LinearBasicDisplay"

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
        "location": make_location(f'{fileName}.bai', protocol),
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
      "faiLocation": make_location(f'{fileName}.fai', protocol)
    }

  # Bgzipped fasta 
  if bool(re.search(fastaGz, fileName)):

    return {
      "type": "BgzipFastaAdapter",
      "fastaLocation": make_location(fileName, protocol),
      "faiLocation": make_location(f'{fileName}.fai', protocol),
      "gziLocation": make_location(f'{fileName}.gzi', protocol)
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

# ================== DataFrame Track =================
def check_track_data(df):
  """
  Checks that the track data data frame is a valid data frame with
  the required columns.

  :param df: the data frame with track data. Must have cols 
      refName, start, end, name. The column additional can optionally be 
      include with more feature information. If a score column is 
      present, it will be used and the track will be rendered to display 
      quantitative features.
  """
  if not isinstance(df, pd.DataFrame):
    raise TypeError("Track data must be a DataFrame")
  if not check_columns(df):
    raise TypeError("DataFrame must contain columns: refName, start, end, name.")
  if df.empty:
    raise TypeError("DataFrame must not be empty.")

def check_columns(df):
  """
  Checks wether dataframe contains the required columns.
  Required columns include: refName, start, end, and name. 
  refName: string
  start: number/integer
  end: number/integer
  name: string
  score (optional): number/integer
  The score column is optional.
  
  :param df: DataFrame containing track data
  """
  required = ["refName", "start", "end", "name"]
  return all(col in df for col in required)


def get_from_config_adapter(df):
  features = get_track_data(df)
  return {
    "type": 'FromConfigAdapter',
    "features": features  
  }

def format_feature(feature):
  uniqueId = str(uuid.uuid4().hex)
  feature["uniqueId"] = uniqueId

def get_track_data(df):
  # iterate over every row in the datafram
  # each row should represent a feature
  # add additional data to dataframe
  required = ['refName','start', 'end', 'name', 'additional', 'type']
  df["type"] = ''
  if "additional" not in df:
    df["additional"] = ''
  if "score" in df:
    required.append('score')
  filtered = df[required]
  # add extra params
  rows = filtered.to_dict('records')
  # features = map(format_feature, rows)
  features = []
  for r in rows:
      newFeature = r
      newFeature['uniqueId'] = str(uuid.uuid4().hex)
      features.append(newFeature)
  # features = filtered.to_dict('records').map(lambda f: {
  #   "refName": f["chrom"],
  #   "start": f["start"],
  #   "end": f["end"],
  #   "unique"
  # })
  return features
