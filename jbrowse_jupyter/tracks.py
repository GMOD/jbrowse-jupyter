import re
import uuid
import pandas as pd


def make_location(location, protocol):
    """
    Creates location object given a location and a protocol.
    :param str location: file path
    :param str protocol: protocol, for now only accepting `uri`
    :return: the location subconfiguration
    :rtype: obj
    :raises ValueError: if a protocol other than `uri` is used.

    """
    # elif protocol == "localPath":
    # return { "uri": location, "locationType": "LocalPathLocation"}
    if protocol == "uri":
        return {"uri": location, "locationType": "UriLocation"}
    else:
        raise TypeError(f"invalid protocol {protocol}")


def supported_track_type(track_type):
    """Checks wether or not the given track type is supported."""
    return track_type in {
        "AlignmentsTrack",
        "QuantitativeTrack",
        "VariantTrack",
        "FeatureTrack",
    }


def guess_display_type(track_type, view="LGV"):
    """
    Returns the possible display type to use for a given track type.

    :param str track_type: the type of the track
    :return: the type of the display to use for the given track type
    :rtype: str
    """
    displays = {
        "AlignmentsTrack": "LinearAlignmentsDisplay",
        "VariantTrack": "LinearVariantDisplay",
        "ReferenceSequenceTrack": "LinearReferenceSequenceDisplay",
        "QuantitativeTrack": "LinearWiggleDisplay",
        "FeatureTrack": "LinearBasicDisplay",
    }
    if view == "CGV":
        displays = {
            "VariantTrack": "ChordVariantDisplay",
            "ReferenceSequenceTrack": "LinearReferenceSequenceDisplay",
        }
    if track_type in displays:
        return displays[track_type]
    else:
        if view == "CGV":
            return "ChordVariantDisplay"
        return "LinearBasicDisplay"


def guess_track_type(adapter_type):
    """
    Returns the possible track type to use given an adapter type.

    :param str adapter_type: the type of the adapter
    :return: the type of the track to use for the given an adapter type
    :rtype: str
    """
    known = {
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
    if adapter_type in known:
        return known[adapter_type]
    else:
        return "FeatureTrack"


def guess_adapter_type(file_location, protocol, index="defaultIndex"):
    """
    Creates location object given a location and a protocol.

    :param str file_location: file path
    :param str protocol: protocol, for now only accepting `uri`
    :param str index: (optional) path to index
    :return: the adapter track subconfiguration
    :rtype: obj
    """
    bam = re.compile(r"\.bam$", re.IGNORECASE)
    bed = re.compile(r"\.bed$", re.IGNORECASE)
    bed_tabix = re.compile(r"\.bed\.b?gz$", re.IGNORECASE)
    big_bed = re.compile(r"\.(bb|bigbed)$", re.IGNORECASE)
    big_wig = re.compile(r"\.(bw|bigwig)$", re.IGNORECASE)
    cram = re.compile(r"\.cram$", re.IGNORECASE)
    fasta_idx = re.compile(r"\.(fa|fasta|fna|mfa)$", re.IGNORECASE)
    fasta_gz = re.compile(r"\.(fa|fasta|fna|mfa)\.b?gz$", re.IGNORECASE)
    gff3 = re.compile(r"\.gff3$", re.IGNORECASE)
    gff3_tabix = re.compile(r"\.gff3?\.b?gz$", re.IGNORECASE)
    gtf = re.compile(r"\.gtf$", re.IGNORECASE)
    hic = re.compile(r"\.hic", re.IGNORECASE)
    nclist = re.compile(r"\/trackData.jsonz?$", re.IGNORECASE)
    paf = re.compile(r"\.paf", re.IGNORECASE)
    sizes = re.compile(r"\.sizes$", re.IGNORECASE)
    sparql = re.compile(r"\/sparql$", re.IGNORECASE)
    twobit = re.compile(r"\.2bit$", re.IGNORECASE)
    vcf = re.compile(r"\.vcf$", re.IGNORECASE)
    vcf_gzp = re.compile(r"\.vcf\.b?gz$", re.IGNORECASE)
    vcf_idx = re.compile(r"\.vcf\.idx$", re.IGNORECASE)

    # bam
    if bool(re.search(bam, file_location)):
        return {
            "type": "BamAdapter",
            "bamLocation": make_location(file_location, protocol),
            "index": {
                "location": make_location(f"{file_location}.bai", protocol),
                "indexType": "CSI"
                if (index != "defaultIndex" and index.upper().endswith("CSI"))
                else "BAI",
            },
        }
    # cram
    if bool(re.search(cram, file_location)):
        return {
            "type": "CramAdapter",
            "cramLocation": make_location(file_location, protocol),
            "craiLocation": make_location(f"{file_location}.crai", protocol),
        }

    # gff3
    if bool(re.search(gff3, file_location)):
        return {
            "type": "UNSUPPORTED",
        }

    # gtf
    if bool(re.search(gtf, file_location)):
        return {
            "type": "UNSUPPORTED",
        }

    # gff3 tabix
    if bool(re.search(gff3_tabix, file_location)):
        return {
            "type": "Gff3TabixAdapter",
            "gffGzLocation": make_location(file_location, protocol),
            "index": {
                "location": make_location(f"{file_location}.tbi", protocol),
                "indexType": "TBI",
            },
        }

    # vcf
    if bool(re.search(vcf, file_location)):
        return {
            "type": "VcfAdapter",
            "vcfLocation": make_location(file_location, protocol),
        }

    # vcf idx
    if bool(re.search(vcf_idx, file_location)):
        return {
            "type": "UNSUPPORTED",
        }

    # vcf gzipped
    if bool(re.search(vcf_gzp, file_location)):
        return {
            "type": "VcfTabixAdapter",
            "vcfGzLocation": make_location(file_location, protocol),
            "index": {
                "location": make_location(f"{file_location}.tbi", protocol),
                "indexType": "CSI"
                if (index != "defaultIndex" and index.upper().endswith("CSI"))
                else "TBI",
            },
        }

    # bigwig
    if bool(re.search(big_wig, file_location)):
        return {
            "type": "BigWigAdapter",
            "bigWigLocation": make_location(file_location, protocol),
        }
    # bed
    if bool(re.search(bed, file_location)):
        return {
            "type": "UNSUPPORTED",
        }

    # bed gz
    if bool(re.search(bed_tabix, file_location)):
        return {
            "type": "BedTabixAdapter",
            "bedGzLocation": make_location(file_location, protocol),
            "index": {
                "location": make_location(f"{file_location}.tbi", protocol),
                "indexType": "CSI"
                if (index != "defaultIndex" and index.upper().endswith("CSI"))
                else "TBI",
            },
        }

    # bigbed
    if bool(re.search(big_bed, file_location)):
        return {
            "type": "BigBedAdapter",
            "bigBedLocation": make_location(file_location, protocol),
        }

    # fasta indexed
    if bool(re.search(fasta_idx, file_location)):
        fai = index if index != "defaultIndex" else f"{file_location}.fai"
        return {
            "type": "IndexedFastaAdapter",
            "fastaLocation": make_location(file_location, protocol),
            "faiLocation": make_location(fai, protocol),
        }

    # Bgzipped fasta
    if bool(re.search(fasta_gz, file_location)):
        return {
            "type": "BgzipFastaAdapter",
            "fastaLocation": make_location(file_location, protocol),
            "faiLocation": make_location(f"{file_location}.fai", protocol),
            "gziLocation": make_location(f"{file_location}.gzi", protocol),
        }

    # twobit
    if bool(re.search(twobit, file_location)):
        return {
            "type": "TwoBitAdapter",
            "twoBitLocation": make_location(file_location, protocol),
        }
    # sizes
    if bool(re.search(sizes, file_location)):
        return {
            "type": "UNSUPPORTED",
        }
    # nclist
    if bool(re.search(nclist, file_location)):
        return {
            "type": "NCListAdapter",
            "rootUrlTemplate": make_location(file_location, protocol),
        }

    # sparql
    if bool(re.search(sparql, file_location)):
        return {
            "type": "SPARQLAdapter",
            "endpoint": make_location(file_location, protocol),
        }
    # hic
    if bool(re.search(hic, file_location)):
        return {
            "type": "HicAdapter",
            "hicLocation": make_location(file_location, protocol),
        }

    # paf
    if bool(re.search(paf, file_location)):
        return {
            "type": "PAFAdapter",
            "pafLocation": make_location(file_location, protocol),
        }

    return {
        "type": "UNKNOWN",
    }


# ================== DataFrame Track =================


def check_track_data(df):
    """
    Checks that data frame is a valid data frame with.

    :param df: the data frame with track data.
    :return: whether or not df is a valid data frame for the track.
    :rtype: boolean
    :raises TypeError:
       if df is not a valid data frame
       if df data frame is empty
       if df does not have the required columns (refName, start, end, name)
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("Track data must be a DataFrame")

    if df.empty:
        raise TypeError("DataFrame must not be empty.")

    if not check_columns(df):
        raise TypeError("DataFrame must contain all required columns.")

    ref_names = df.dtypes["refName"]
    names = df.dtypes["name"]
    start = df.dtypes["start"]
    end = df.dtypes["end"]
    correct_string = ref_names == object and names == object
    correct_numbers = start == int and end == int
    if not (correct_numbers and correct_string):
        col_err = "One or more columns do not have the correct data type."
        raise TypeError(col_err)


def check_columns(df):
    """
    Checks wether dataframe contains the required columns.

    :param df: the data frame with track data.
    :return: whether or not df contains all the required columns.
            required columns: refName, start, end, name, score (is optional)
    :rtype: boolean
    """
    required = ["refName", "start", "end", "name"]
    return all(col in df for col in required)


def get_from_config_adapter(df):
    """
    Creates a FromConfigAdapter adapter subconfiguration to
    use in the data frame track configuration.

    :param df: the data frame with track data.
    :return: the adapter subconfiguration
    :rtype: obj
    """
    features = get_track_data(df)
    return {"type": "FromConfigAdapter", "features": features}


def format_feature(feature):
    """Adds a uniqueId to the given featyre."""
    unique_id = str(uuid.uuid4().hex)
    feature["uniqueId"] = unique_id


def get_track_data(df):
    """
    Retrieves the features from the data frame.

    :param df: the data frame with track data.
    :return: features
    :rtype: ist[obj]
    """
    required = ["refName", "start", "end", "name", "additional", "type"]
    df["type"] = ""
    df["additional"] = ""
    if "score" in df:
        required.append("score")
        if df.dtypes["score"] != int:
            raise TypeError("Score column must be an integer")
    filtered = df[required]
    rows = filtered.to_dict("records")
    features = []
    for r in rows:
        newFeature = r
        newFeature["uniqueId"] = str(uuid.uuid4().hex)
        features.append(newFeature)
    return features
