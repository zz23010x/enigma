def PrintLogRequestsGet(url, params=None):
    from public.LogHelper import logger
    geturl = ''
    if not params is None:
        geturl = ''.join([key + '=' + str(val) + '&' for key, val in params.items()])
        if geturl[-1] is '&':
            geturl = '?' + geturl[:-1]
    logger().info('requests get:{0}{1}'.format(url, geturl))