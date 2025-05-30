﻿using NewEnergyHackathon.Web.Services;
using Python.Runtime;

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.
builder.Services.AddControllersWithViews();

builder.Services.AddHttpClient();
builder.Services.AddSingleton<INedService, NedService>();
builder.Services.AddSingleton<ISmartMeterService, SmartMeterService>();
builder.Services.AddSingleton<IBenCompareService, BenCompareService>();
builder.Services.AddMemoryCache();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (!app.Environment.IsDevelopment())
{
  app.UseExceptionHandler("/Home/Error");
  // The default HSTS value is 30 days. You may want to change this for production scenarios, see https://aka.ms/aspnetcore-hsts.
  app.UseHsts();
}

app.UseHttpsRedirection();
app.UseRouting();

PythonEngine.Initialize();
PythonEngine.BeginAllowThreads();

app.UseAuthorization();

app.UseStaticFiles();

app.MapControllerRoute(
    name: "default",
    pattern: "{controller=Home}/{action=Index}/{id?}");
    //.WithStaticAssets(); //Not working in .NET 8


app.Run();
