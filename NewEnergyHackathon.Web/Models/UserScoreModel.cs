namespace NewEnergyHackathon.Web.Models;

public class UserScoreWrapper
{
  public List<UserScoreData> Data { get; set; }
  public double PercentageOfUserDailyGreenConsumption { get; set; }
  public double PercentageOfGridDailyGreenConsumption { get; set; }
}

public class UserScoreData
{
  public string ValidFrom { get; set; }
  public double Volume_Solar { get; set; }
  public double Volume_Wind { get; set; }
  public double Volume_TotalMix { get; set; }
  public string Items_Timestamp_UTC { get; set; }
  public double ConsumptionDeliveryTotal { get; set; }
  public double Solar_Percentage { get; set; }
  public double Wind_Percentage { get; set; }
  public double TotalGreen_Percentage { get; set; }
  public double TotalNoGreen_Percentage { get; set; }
  public double ConsumptionDeliveryTotal_Green { get; set; }
  public double ConsumptionDeliveryTotal_NoGreen { get; set; }
}