META_SITE_PROTOCOL = "https"
META_SITE_DOMAIN = "{{project_name}}.ch"
META_USE_OG_PROPERTIES = True
META_SITE_TYPE = "website"

PAGE_META_DESCRIPTION_LENGTH = 160


# DEFAULTS
DJANGO_CHECK_SEO_SETTINGS = {
    "content_words_number": [300, 600],
    "internal_links": 1,
    "external_links": 1,
    "meta_title_length": [30, 60],
    "meta_description_length": [50, PAGE_META_DESCRIPTION_LENGTH],
    "keywords_in_first_words": 50,
    "max_link_depth": 4,
    "max_url_length": 70,
}
