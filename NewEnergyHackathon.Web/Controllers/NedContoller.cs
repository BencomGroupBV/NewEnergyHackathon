using Microsoft.AspNetCore.Mvc;
using NewEnergyHackathon.Web.Services;

namespace NewEnergyHackathon.Web.Controllers;

[ApiController]
public class NedContoller(INedService nedService) : Controller
{
  [HttpGet("results")]
  public async Task<IActionResult> GetResults([FromQuery] List<int> typeIds, DateOnly before, DateOnly after)
  {
    typeIds = new List<int>
    {
      1,  // Wind
      2,  // Solar
      17, // WindOffShore
      18, // FossilGasPower
      19, // FossilHardCoal
      20, // Nuclear
      21, // WastePower
      22, // WindOffshoreB
      25, // BiomassPower
      26, // OtherPower
      27, // ElectricityMix
      35, // CHPTotal
      51, // WindOffshoreC
      59  // ElectricityLoad
    };

    var results = await nedService.GetResultsAsync(typeIds, before, after);

    return Ok(results);
  }
}
