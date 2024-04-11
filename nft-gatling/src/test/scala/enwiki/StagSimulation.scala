package enwiki

import io.gatling.core.Predef._
import io.gatling.http.Predef._

import java.io.File
import com.typesafe.config.{Config, ConfigFactory}

import scala.concurrent.duration.DurationInt

class StagSimulation extends Simulation {
  val configPath = "src\\test\\resources\\"
  val config = ConfigFactory.parseFile(new File(configPath + "application.conf"))
  val baseUrl = config.getString("conf.baseUrl")

  val credentialsFile = config.getString("conf.credentials")
  val credentials = ConfigFactory.parseFile(new File(configPath + credentialsFile))
  val username = credentials.getString("credentials.username")
  val password = credentials.getString("credentials.password")

  val ratesFile = config.getString("conf.rates")
  val rates = ConfigFactory.parseFile(new File(configPath + ratesFile))
  val searchRate = rates.getString("rates.search").toInt
  val searchCircle = rates.getString("rates.searchCircle").toInt

  val httpProtocol = http.baseUrl(baseUrl)
  val searchTerms = csv(configPath + "search_terms.csv").eager.circular
  val users = csv(configPath + "users.csv").random
  val sentHeaders = Map("Accept-Language" -> "en-US,en;q=0.8",
    "Accept" -> "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Encoding" -> "deflate,sdch",
    "User-Agent" -> "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

  val stagEnwikiSearch = scenario("stagEnwikiSearch")

    .feed(users).exec(
    http("Impersonation")
      .get("/getzvuz.jsp")
      .headers(sentHeaders)
      .queryParam("zvuvId", "${cNumber}")
      .basicAuth(username, password).check(status.is(200))
  )
    .repeat(searchCircle) {
      feed(searchTerms).pace(searchRate.seconds).exec(http("Search")
        .get("/wiki/dosearchsite.action")
        .headers(sentHeaders)
        .queryParam("cql", "siteSearch+~+\"${searchTerm}\"")
        .check(status.is(200)))
    }
  //  setUp(stagEnwikiSearch.inject(constantUsersPerSec(1) during(20))).protocols(httpProtocol)
  setUp(stagEnwikiSearch.inject(atOnceUsers(1))).protocols(httpProtocol)
}
