repo_overview: str = """
query getOverview($year: DateTime!){
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
    pinnedItems {
      totalCount
    }
    repositories {
      totalCount
    }
    contributionsCollection(from: $year) {
      contributionCalendar {
        totalContributions
      }
    }
  }
}
"""
