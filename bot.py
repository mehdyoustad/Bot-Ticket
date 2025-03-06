import discord
import json
import os
from discord.ext import commands
from dotenv import load_dotenv

# 📌 Charger les variables d'environnement depuis .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID"))
CATEGORY_ID = int(os.getenv("CATEGORY_ID"))
ADMIN_ROLE_ID = int(os.getenv("ADMIN_ROLE_ID"))

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
        try:
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

        except Exception as e:
            print(f"⚠️ Erreur lors de la création du ticket : {e}")

bot.run(TOKEN)
