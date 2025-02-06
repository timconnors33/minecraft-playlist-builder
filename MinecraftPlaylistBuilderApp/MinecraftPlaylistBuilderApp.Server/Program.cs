using Microsoft.EntityFrameworkCore;
using MinecraftPlaylistBuilderApp.Server;
using MinecraftPlaylistBuilderApp.Server.Interfaces;
using MinecraftPlaylistBuilderApp.Server.Repositories;
using MinecraftPlaylistBuilderApp.Server.Services;

var AllowedOrigins = "_allowedOrigins";

var builder = WebApplication.CreateBuilder(args);

// Add services to the container.

builder.Services.AddControllers();
// Learn more about configuring OpenAPI at https://aka.ms/aspnet/openapi
builder.Services.AddOpenApi();

var connectionString = builder.Configuration.GetConnectionString("DatabaseConnection");
builder.Services.AddDbContext<MinecraftPlaylistBuilderDbContext>(options => options.UseSqlServer(connectionString));
builder.Services.AddScoped<ISeriesRepository, SeriesRepository>();
builder.Services.AddScoped<ISeriesService, SeriesService>();
builder.Services.AddControllers();

// https://learn.microsoft.com/en-us/aspnet/core/security/cors?view=aspnetcore-9.0
// TODO: See about which origin(s) to allow in production
builder.Services.AddCors(options =>
{
    options.AddPolicy(name: AllowedOrigins,
        policy =>
        {
            policy.WithOrigins("https://localhost:51252");
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
}

app.UseHttpsRedirection();

// Needs to be in a specific spot in the middleware order.
// See the link above the call to the AddCors() method.
app.UseCors(AllowedOrigins);

app.UseAuthorization();

app.MapControllers();

app.MapFallbackToFile("/index.html");

app.Run();
