from urllib.parse import urlparse

def get_features_for_url(url):
    url_domain, url_directory, url_file, url_query = get_url_parts(url)
    # print(url_domain)
    # print(url_directory)
    # print(url_file)
    # print(url_query)

    # Features for the whole url
    features = get_counts(url)

    # qty_tld_url
    # TODO: Not sure how to get the tld
    features.append(3)

    # length_url
    features.append(len(url))

    # email_in_url
    # TODO: Find if email exists in a string
    features.append(0)

    # Features on domain URL
    features.extend(get_counts(url_domain))

    # qty_vowels_domain
    num_vowels = 0
    for v in "aeiou":
        num_vowels += url_domain.count(v)
    features.append(num_vowels)

    # domain_length
    features.append(len(url_domain))

    # TODO: domain_in_ip
    features.append(0)

    # server_client_domain
    s_c_in_domain = "server" in url_domain or "client" in url_domain
    features.append(1 if s_c_in_domain else 0)

    # Features on directory
    features.extend(get_counts(url_directory))

    # directory_length
    features.append(len(url_directory))

    # Features on file-name
    features.extend(get_counts(url_file))

    # file_length
    features.append(len(url_file))

    # Features on query-params
    features.extend(get_counts(url_query))

    # Params Length
    features.append(len(url_query))

    # TODO: tld_present_params - TLDpresent in parameters
    features.append(0)

    # TODO: qty_params - Number of parameters
    features.append(0)

    # TODO: The additional features come here (more on this later)

    return features

def count_chars_in_str(s, chars_list):
    return [s.count(c) for c in chars_list]

def get_counts(s):
    res = count_chars_in_str(
            s, 
            [
                # qty_dot_url
                ".",
                # qty_hyphen_url
                "-",
                # qty_underline_url
                "_",
                # qty_slash_url
                "/",
                # qty_questionmark_url
                "?",
                # qty_equal_url
                "=",
                # qty_at_url
                "@",
                # qty_and_url
                "&",
                # qty_exclamation_url
                "!",
                # qty_space_url
                " ",
                # qty_tilde_url
                "~",
                # qty_comma_url
                ",",
                # qty_plus_url
                "+",
                # qty_asterisk_url
                "*",
                # qty_hashtag_url
                "#",
                # qty_dollar_url
                "$",
                # qty_percent_url
                "%",
                ]
            )
    return res

def get_url_parts(url):
    parsed_res = urlparse(url)

    # Split path into directory and file
    path = parsed_res.path

    dir_part = ""
    file_part = ""
    path_parts = [p for p in path.split("/") if p]
    if len(path_parts) > 0:
        file_part = path_parts.pop(-1)
        if len(path_parts) == 0:
            dir_part = ""
        else:
            dir_part = "/".join(path_parts)

    return [
            parsed_res.netloc, # Domain and subdomain
            dir_part,
            file_part,
            parsed_res.query
            ]


def test_get_url_parts():
    samples = {
            "https://example.com/examples/index.php?q=example&y=2020": ["example.com", "examples", "index.php", "q=example&y=2020"],
            "https://example.com/index.php?q=example&y=2020": ["example.com", "", "index.php", "q=example&y=2020"],
            "https://example.com/?q=example&y=2020": ["example.com", "", "", "q=example&y=2020"],
            "https://example.com/": ["example.com", "", "", ""],
            }

    for link, expected in samples.items():
        assert get_url_parts(link) == expected

if __name__ == "__main__":
    # A quick test
    test_get_url_parts()

    url = "https://example.com/examples/index.php?q=example&y=2020"

    # Get the features
    features = get_features_for_url(url)
    print(features)
    print(len(features))
