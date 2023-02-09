repo_overview: str = """
query getOverview{
  viewer {
    login
    followers {
      totalCount
    }
    following {
      totalCount
    }
    starredRepositories {
      totalCount
    }
    pinnedItems(first: 6) {
      edges {
        node {
          ... on Repository {
            id
            name
          }
        }
      }
    }
  }
}
"""
