from urllib.parse import urlparse
from email.utils import parseaddr
import ipaddress

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

    # TODO: email_in_url
    # Find if email exists in a string
    has_email = 0
    if does_str_have_email(url):
        has_email = 1
    print("Does email exist", has_email)
    features.append(has_email)

    # Features on domain URL
    features.extend(get_counts(url_domain))

    # qty_vowels_domain
    num_vowels = 0
    for v in "aeiou":
        num_vowels += url_domain.count(v)
    features.append(num_vowels)

    # domain_length
    features.append(len(url_domain))

    # domain_in_ip
    has_ip_in_domain = 0
    if does_domain_have_ip(url_domain):
        has_ip_in_domain = 1
    features.append(has_ip_in_domain)

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

    # qty_params - Number of parameters
    features.append(url_query.count("&"))

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

def does_str_have_email(s):
    # TODO: Change this
    return not parseaddr(s)[1].strip() == ''


def does_domain_have_ip(url_domain):
    try:
        domain_val = url_domain
        if domain_val.count(":") == 1:
            domain_val = domain_val.split(":")[0]
        ip = ipaddress.ip_address(domain_val)
    except:
        return False
    else:
        return True

def test_get_url_parts():
    samples = {
            "https://example.com/examples/index.php?q=example&y=2020": ["example.com", "examples", "index.php", "q=example&y=2020"],
            "https://example.com/index.php?q=example&y=2020": ["example.com", "", "index.php", "q=example&y=2020"],
            "https://example.com/?q=example&y=2020": ["example.com", "", "", "q=example&y=2020"],
            "https://example.com/": ["example.com", "", "", ""],
            }

    for link, expected in samples.items():
        assert get_url_parts(link) == expected

def test_ip_in_url():
    samples = {
            "https://192.1.0.1/examples/index.php?q=example&y=2020": True,
            "https://192.1.0.1:8199/examples/index.php?q=example&y=2020": True,
            "https://example.com/examples/index.php?q=example&y=2020":False,
            "https://example.com/index.php?q=example&y=2020": False,
            "https://example.com/?q=example&y=2020": False,
            "https://example.com/": False,
            }

    for link, expected in samples.items():
        parts = get_url_parts(link)
        assert does_domain_have_ip(parts[0]) == expected

if __name__ == "__main__":
    # A quick test
    test_get_url_parts()
    test_ip_in_url()

    url = "https://example.com/examples/index.php?q=example&y=2020"

    # Get the features
    features = get_features_for_url(url)
    print(features)
    print(len(features))
