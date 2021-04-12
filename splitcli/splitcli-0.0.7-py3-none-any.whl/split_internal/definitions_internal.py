from splitcli.split_apis import splits_api, definitions_api

def force_calculation(session, org_id, workspace_id, environment_name, split_name):
	definition = definitions_api.get(workspace_id, environment_name, split_name)
	print(definition)
	definition_id = definition['id']
	version = definition['lastUpdateTime']
	url = f"https://app.split.io/internal/api/organization/{org_id}/metrics/results/tests/{definition_id}/version/{version}/force"
	session.get(url, headers={'Split-CSRF': session.cookies['split-csrf']})

def get_metadata(session):
	url ='https://app.split.io/internal/api/testMetadata/organization/{org_id}?query={name}'
	curl '' \
  -H 'Connection: keep-alive' \
  -H 'sec-ch-ua: "Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"' \
  -H 'DNT: 1' \
  -H 'Split-CSRF: v1::94781e2afd2f0253b9e24e3a43271460' \
  -H 'sec-ch-ua-mobile: ?0' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36' \
  -H 'Accept: */*' \
  -H 'Sec-Fetch-Site: same-origin' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Referer: https://app.split.io/org/d4f294b0-98cc-11eb-a694-128f4a94c92f/ws/d4fddf50-98cc-11eb-a694-128f4a94c92f/splits/cc434b20-98ef-11eb-8363-1690990a9bbb/env/d50188d0-98cc-11eb-a694-128f4a94c92f/metrics/results' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  -H 'Cookie: ajs_user_id=%222dc99870-c63d-11e6-9e87-123991f9470a%22; ajs_group_id=%224d3405a0-9ca5-11e5-9706-16a11fb02dec%22; G_ENABLED_IDPS=google; ajs_anonymous_id=%226826c778-e4fc-4861-a186-028ba02e0f51%22; __zlcmid=107jQTTyb7hlBNr; _gcl_au=1.1.1262812159.1611765069; _ga=GA1.2.936468261.1611765069; _fbp=fb.1.1611765069652.251027281; _hly_vid=48f32f72-87fc-4e71-84e0-3ee3eb5a052a; _hjTLDTest=1; _hjid=f5d40a1f-dcb8-4439-9573-26eb58ce7356; hubspotutk=e3f779229ee8c4e8254bd2fe6c490f7f; __hssrc=1; SSESS8261f180aef150d2b7536d831b6bb571=910d9161d7bf5ba96b495c06a66d12ac; G_AUTHUSER_H=0; split-legacy-jwt=eyJhbGciOiJIUzUxMiIsImNhbGciOiJERUYifQ.eNqqViouTVKyUspIzSuqdCguyMks0cvMV9JRyiwuBgrDBPTLDIFiqRUFSlaGZobmlhbmZqbmtQAAAAD__w.nF8H8CB2y9JWMZMCOPthvH7OetmjqSnwJ09BUhGezi7XVLNcF7Lh3CX2wpcQqMqG3oPFpKybx3Giorop1BYCGw; split-legacy-csrf=v1::14241d65857faabdfce86ab2e6d3b285; __hstc=199948401.e3f779229ee8c4e8254bd2fe6c490f7f.1611765070404.1617230546217.1617901966445.45; _uetvid=0fd5532060bd11eb96da4bfd8ed56147; split-csrf=v1::94781e2afd2f0253b9e24e3a43271460; split-jwt=eyJhbGciOiJIUzUxMiIsImNhbGciOiJERUYifQ.eNoMylEKgCAMANC77LuVsyWz26hNEIIEK4Lo7vn7eC-0K8IKG6tqnA16SQmJNGJwnpGsZA6ek7cZBiit9dzqXs6xHNNN3fSpsJIjMXYxLN8PAAD__w.AgIcZLvJfP-Kqg7FxenTPjRw8zrtEJE-OciKf2DzZmnwFQGjdlKdJCM6-pUDalFQDi2rruUnfPfmaJJX-EnnQg' \
  --compressed