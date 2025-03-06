import discord
import json
import os
from discord.ext import commands

TOKEN = "MTM0NzMxODMyMjAxNzk5Njg4MQ.GXqsLX.z_EiBHSbYroN6yE2E6QYLROYaa_Uk8NCu9f9a8"
GUILD_ID = 1326517206674182235  # Remplace par l'ID de ton serveur
CATEGORY_ID = 1326661110815789130  # Remplace par l'ID de la catégorie où créer les salons
ADMIN_ROLE_ID = 1326518471923863656  # Remplace par l'ID du rôle admin qui doit voir les salons

# 📌 Fichier pour stocker le compteur de tickets
TICKET_FILE = "ticket_counter.json"

# Vérifier si le fichier existe, sinon initialiser à 38
if not os.path.exists(TICKET_FILE):
    with open(TICKET_FILE, "w") as f:
        json.dump({"counter": 38}, f)

# Charger le compteur actuel
with open(TICKET_FILE, "r") as f:
    data = json.load(f)
    ticket_counter = data["counter"]

intents = discord.Intents.default()
intents.members = True  # Active la détection des nouveaux membres

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot connecté en tant que {bot.user}")

@bot.event
async def on_member_join(member):
    global ticket_counter

    guild = bot.get_guild(GUILD_ID)
    category = bot.get_channel(CATEGORY_ID)
    admin_role = guild.get_role(ADMIN_ROLE_ID)

    if category and admin_role:
        # Générer le nom du ticket avec l'incrémentation
        ticket_name = f"ticket-{ticket_counter}"

        # Création des permissions
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),  # Bloque tout le monde
            member: discord.PermissionOverwrite(read_messages=True, send_messages=True),  # Autorise le membre
            admin_role: discord.PermissionOverwrite(read_messages=True, send_messages=True)  # Autorise les admins
        }

        # Création du salon textuel privé
        channel = await guild.create_text_channel(
            name=ticket_name,
            category=category,
            overwrites=overwrites
        )

        # Envoyer un message de bienvenue et d'instructions
        await channel.send(
            f"Bienvenue {member.mention} ! 🎉\n"
            f"Merci de renseigner les informations nécessaires en référence au salon **#tout-savoir**."
        )

        # Incrémenter et sauvegarder le compteur
        ticket_counter += 1
        with open(TICKET_FILE, "w") as f:
            json.dump({"counter": ticket_counter}, f)

bot.run(TOKEN)
