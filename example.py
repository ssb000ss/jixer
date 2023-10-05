def netlas_test(engines):
    engine_arg = '-n'
    query = 'http.favicon.hash_sha256:50836e4dd679302c8477bb1cc3667a605f16d998709ef2f68ed1fb9d2be8ea7d AND geo.country:SN'
    engine = engines.get(engine_arg)
    engine.search_and_save_ip_list(query)


def zoomeye_test(engines):
    engine_arg = '-z'
    engine = engines.get(engine_arg)
    engine.count(query)
    engine.search_and_save_ip_list(query)


def fofa_test(engines):
    engine_arg = '-f'
    query = 'icon_hash="2141724739" && country="SN"'
    engine = engines.get(engine_arg)
    engine.search_and_save_ip_list(query)
