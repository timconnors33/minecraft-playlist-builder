// Authentication code based on examples provided by https://github.com/Azure-Samples/ms-identity-ciam-javascript-tutorial.git

using System.Security.Cryptography;
using Microsoft.EntityFrameworkCore;
using Microsoft.Net.Http.Headers;
using MinecraftPlaylistBuilderApp.Server;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Repositories;
using MinecraftPlaylistBuilderApp.Server.Services;
using Microsoft.AspNetCore.Authentication.JwtBearer;
using Microsoft.Identity.Web;
using MinecraftPlaylistBuilderApp.Server.Models;

var AllowedOrigins = "_allowedOrigins";

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddHttpContextAccessor();

builder.Services.AddAuthentication(JwtBearerDefaults.AuthenticationScheme)
        .AddMicrosoftIdentityWebApi(options =>
        {
            builder.Configuration.Bind("AzureAd", options);
            options.Events = new JwtBearerEvents();

            /*
            options.Events.OnTokenValidated = async context =>
            {
                string[] allowedClientApps = { "5449bd54-0d95-4bde-a7dc-051ce631d03b" };

                string clientappId = context?.Principal?.Claims
                    .FirstOrDefault(x => x.Type == "azp" || x.Type == "appid")?.Value;

                if (!allowedClientApps.Contains(clientappId))
                {
                    throw new System.Exception("This client is not authorized");
                }
            };
            */
        }, options => { builder.Configuration.Bind("AzureAd", options); });

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

var connectionString = builder.Configuration.GetConnectionString("DatabaseConnection");
builder.Services.AddDbContext<MinecraftPlaylistBuilderDbContext>(options => options.UseSqlServer(connectionString));

builder.Services.AddScoped<ISeriesRepository, SeriesRepository>();
builder.Services.AddScoped<ISeriesService, SeriesService>();

builder.Services.AddScoped<ISeasonRepository, SeasonRepository>();
builder.Services.AddScoped<ISeasonService, SeasonService>();

builder.Services.AddScoped<IChannelRepository, ChannelRepository>();
builder.Services.AddScoped<IChannelService, ChannelService>();

builder.Services.AddScoped<IVideoRepository, VideoRepository>();
builder.Services.AddScoped<IVideoService, VideoService>();

builder.Services.AddScoped<ISeasonAppearanceRepository, SeasonAppearanceRepository>();
builder.Services.AddScoped<ISeasonAppearanceService, SeasonAppearanceService>();

builder.Services.AddScoped<IPlaylistRepository, PlaylistRepository>();
builder.Services.AddScoped<IPlaylistService, PlaylistService>();

builder.Services.AddControllers();

// https://learn.microsoft.com/en-us/aspnet/core/security/cors?view=aspnetcore-9.0
// TODO: See about which origin(s) and permissions to allow in production, if any
builder.Services.AddCors(options =>
{
    options.AddPolicy(name: AllowedOrigins,
        policy =>
        {
            policy.WithOrigins("https://localhost:51252");
            policy.AllowAnyMethod();
            policy.AllowAnyHeader();
            policy.AllowCredentials();
        });
});

var app = builder.Build();

app.UseDefaultFiles();
app.MapStaticAssets();

// Configure the HTTP request pipeline.
// TODO: Comment these lines commented out or no?
if (app.Environment.IsDevelopment())
{
    app.MapOpenApi();
    app.UseDeveloperExceptionPage();
}
else
{
    app.UseHsts();
}

// Needs to be in a specific spot in the middleware order.
// See the link above the call to the AddCors() method.
app.UseCors(AllowedOrigins);
app.UseHttpsRedirection();

app.UseRouting();
app.UseAuthentication();
app.UseAuthorization();

app.MapControllers();

app.MapFallbackToFile("/index.html");

app.Run();
