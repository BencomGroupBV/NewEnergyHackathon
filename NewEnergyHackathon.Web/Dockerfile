# See https://aka.ms/customizecontainer to learn how to customize your debug container and how Visual Studio uses this Dockerfile to build your images for faster debugging.

# This stage is used when running from VS in fast mode (Default for Debug configuration)
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS base
USER root

# Install Python 3.11 and dependencies
RUN apt-get update && apt-get install -y \
    python3.11 python3.11-venv python3-pip libpython3.11 \
    && python3.11 -m venv /opt/venv \
    && /opt/venv/bin/pip install --upgrade pip \
    && /opt/venv/bin/pip install pandas

# Set environment variables for Python.NET
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONNET_PYDLL=/usr/lib/x86_64-linux-gnu/libpython3.11.so
ENV PYTHONHOME=/usr
#ENV DOTNET_EnableDiagnostics=0

WORKDIR /app
EXPOSE 8080
EXPOSE 8081


# This stage is used to build the service project
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["NewEnergyHackathon.Web.csproj", "."]
RUN dotnet restore "./NewEnergyHackathon.Web.csproj"
COPY . .
WORKDIR "/src/."
RUN dotnet build "./NewEnergyHackathon.Web.csproj" -c $BUILD_CONFIGURATION -o /app/build

# This stage is used to publish the service project to be copied to the final stage
FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "./NewEnergyHackathon.Web.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

# This stage is used in production or when running from VS in regular mode (Default when not using the Debug configuration)
FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "NewEnergyHackathon.Web.dll"]