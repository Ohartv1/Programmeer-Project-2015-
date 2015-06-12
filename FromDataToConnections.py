import json

with open('Data.json', 'r') as data_file:    
    data = json.load(data_file)

list_nodes = []
list_titles = []
for dic in data:
	list_titles.append(dic.get("title"))
	dict_nut = {}
	dict_nut.update({"name": dic.get("title"), \
		"num_cit": len(dic.get("cited_by")), \
		"generation": dic.get("generation")})
	list_nodes.append(dict_nut)

for dic in data:
	for cit in dic.get("cited_by"):
		if not cit in list_titles:
			dict_nut = {}
			dict_nut.update({"name": cit, \
				"num_cit": 0, \
				"generation": dic.get("generation") + 1})
			list_nodes.append(dict_nut)
			list_titles.append(cit)


list_connections = []
for each in data:
	for every in each.get("cited_by"):
		new_dict = {}
		temp = each.get("title")
		new_dict.update({"source": list_titles.index(temp), \
			"target": list_titles.index(every)})
		list_connections.append(new_dict)

final_connections = []
for iets in list_connections:
	if not iets in final_connections:
		final_connections.append(iets)



return_dict = {}
return_dict.update({"nodes": list_nodes})
return_dict.update({"links": list_connections})


with open("Connections.json", "a") as outfile:
    json.dump(return_dict, outfile, indent=2)