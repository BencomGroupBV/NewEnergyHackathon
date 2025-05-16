using System.Text.Json.Serialization;

namespace NewEnergyHackathon.Web.Models;

public class BencompareUsage
{
  [JsonPropertyName("")]
  public int EmptyKey { get; set; }

  [JsonPropertyName("Items_Timestamp_UTC_date")]
  public string ItemsTimestampUTCDate { get; set; }

  [JsonPropertyName("Items_Timestamp_UTC")]
  public string ItemsTimestampUTC { get; set; }

  [JsonPropertyName("Items_ConsumptionDeliveryTotal")]
  public double ItemsConsumptionDeliveryTotal { get; set; }
}
