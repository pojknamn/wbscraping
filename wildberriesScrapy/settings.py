# Scrapy settings for wildberriesScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'wildberriesScrapy'

SPIDER_MODULES = ['wildberriesScrapy.spiders']
NEWSPIDER_MODULE = 'wildberriesScrapy.spiders'



# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32


# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# PROXY_POOL_ENABLED = True
# # 'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
# #     'scrapy_user_agents.middlewares.RandomUserAgentMiddleware': 400,
# DOWNLOADER_MIDDLEWARES = {
#     'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610,
#     'scrapy_proxy_pool.middlewares.BanDetectionMiddleware': 620,
# }


