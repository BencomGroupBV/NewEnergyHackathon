using System.Text.Json;
using NewEnergyHackathon.Web.Models.Enums;

namespace NewEnergyHackathon.Web.Services;

public interface INedService
{
  Task<string> GetGridConsumptionByEnergyType(EnergyType energyType, DateOnly dateTo, DateOnly dateFrom);
}

public class NedService : INedService
{
  private readonly HttpClient _httpClient;
  private const string BaseUrl = "https://api.ned.nl/v1/utilizations";

  public NedService(HttpClient httpClient)
  {
    _httpClient = httpClient;
    _httpClient.DefaultRequestHeaders.Clear();
    _httpClient.DefaultRequestHeaders.Add("X-AUTH-TOKEN",
      "a1997970697c96b6513b010c15e586c769eb33d5281064c5bffb5c9c24d48464");
    _httpClient.DefaultRequestHeaders.Add("Accept", "application/ld+json");
  }

  public async Task<string> GetGridConsumptionByEnergyType(EnergyType energyType, DateOnly dateTo, DateOnly dateFrom)
  {
    var allResults = new List<JsonElement>();

    var queryParams = new Dictionary<string, string>
    {
    { "point", "0" },
    { "type", ((int)energyType).ToString() },
    { "granularity", "4" },
    { "granularitytimezone", "1" },
    { "classification", "2" },
    { "activity", "1" },
    { "validfrom[strictly_before]", dateTo.ToString("yyyy-MM-dd") },
    { "validfrom[after]", dateFrom.ToString("yyyy-MM-dd") }
    };

    var requestUrl = $"{BaseUrl}?{await new FormUrlEncodedContent(queryParams).ReadAsStringAsync()}";

    while (!string.IsNullOrEmpty(requestUrl))
    {
      var response = await _httpClient.GetAsync(requestUrl);
      response.EnsureSuccessStatusCode();

      var content = await response.Content.ReadAsStringAsync();
      using var doc = JsonDocument.Parse(content);
      var root = doc.RootElement;

      if (root.TryGetProperty("hydra:member", out var members))
      {
        allResults.AddRange(members.EnumerateArray()
          .Select(item => JsonDocument
            .Parse(item.GetRawText()).RootElement.Clone()));
      }

      if (root.TryGetProperty("hydra:view", out var view) &&
        view.TryGetProperty("hydra:next", out var nextPage))
      {
        requestUrl = "https://api.ned.nl" + nextPage.GetString();
      }
      else
      {
        requestUrl = null;
      }
    }

    var options = new JsonSerializerOptions { WriteIndented = true };
    var jsonOutput = JsonSerializer.Serialize(allResults, options);

    return jsonOutput;
  }
}
