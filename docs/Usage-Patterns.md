# Usage Patterns / Recipes

## Purpose
Provide task-oriented patterns with reusable examples.

## Find a concept by label
```bash
curl "https://data.bioontology.org/search?q=melanoma&require_exact_match=true&apikey=YOUR_KEY"
```

## Traverse a class hierarchy
1) Fetch a class resource
2) Follow `links.children` or `links.parents`

```bash
curl "https://data.bioontology.org/ontologies/NCIT/classes/ROOT_ID/children?apikey=YOUR_KEY"
```

## Annotate free text
```bash
curl "https://data.bioontology.org/annotator?text=melanoma&exclude_synonyms=true&longest_only=true&apikey=YOUR_KEY"
```

## Recommend ontologies for a dataset
```bash
curl "https://data.bioontology.org/recommender?input=gene,expression,cell&input_type=2&apikey=YOUR_KEY"
```

## Handle paginated search results
```bash
curl "https://data.bioontology.org/search?q=cancer&page=2&pagesize=25&apikey=YOUR_KEY"
```
