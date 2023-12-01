# -*- coding: utf-8 -*-

from odoo import models, fields, api
import base64
import requests
import requests
from bs4 import BeautifulSoup
import json




class Team(models.Model):
    _name = 'team__manager.team'
    _description = 'team__manager.team'

    name = fields.Char(string='Team Name')
    points = fields.Integer(string='Points', default=0)
    goals_scored = fields.Integer(string='Goals Scored', default=0)
    goals_conceded = fields.Integer(string='Goals Conceded', default=0)
    player_ids = fields.One2many('team__manager.player', 'team_id', string='Players')
    image = fields.Binary(string='Picture', attachment=True)

   
   
    def create_demo_data(self):
        for team_data in self.scrap_teams():
            team_vals = {
            'name': team_data['name'],
            'image': self._get_image_binary(team_data['logo_url']),
            'points': team_data['points'],
            'goals_scored': team_data['goals_scored'],
            'goals_conceded': team_data['goals_conceded'],
           
            # Add other fields as needed
            
         }
            print(team_vals)
            team = self.env['team__manager.team'].create(team_vals)
    def _get_image_binary(self,image_url):
        response = requests.get(image_url)
        if response.status_code == 200:
            return base64.b64encode(response.content)
        return False
    def scrap_teams(self):
        url = "https://botolapro.gestfootball.com/fr/p4746/"  # Replace with the actual URL of the webpage containing the data
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        table_body = soup.find('tbody')
        teams = []

        for row in table_body.find_all('tr'):
            # Extract the team name, logo URL, points, goals scored, and goals conceded from the row
            columns = row.find_all('td')
            team_name = columns[1].text.strip()
            logo_url = columns[1].find('img')['src']
            points = int(columns[2].text.strip())  # Adjusted the column index for points
            goals_scored = int(columns[7].text.strip())  # Adjusted the column index for goals scored
            goals_conceded = int(columns[8].text.strip())  #

            # Append the team data to the list
            teams.append({
                'name': team_name,
                'logo_url': logo_url,
                'points': points,
                'goals_scored': goals_scored,
                'goals_conceded': goals_conceded
            })

        return teams

    def update_or_create_team(self, team_data):
        # Check if the team already exists by searching for it based on the team name
            existing_team = self.env['team__manager.team'].search([('name', '=', team_data['name'])])

            if existing_team:
            # If the team exists, update its information
                existing_team.write({
                    'image': self._get_image_binary(team_data['logo_url']),
                    'points': team_data['points'],
                    'goals_scored': team_data['goals_scored'],
                    'goals_conceded': team_data['goals_conceded'],
                # Add other fields as needed
                })
                print(f"Team {team_data['name']} updated.")
            else:
            # If the team does not exist, create a new team with the scraped data
                team_vals = {
                'name': team_data['name'],
                'image': self._get_image_binary(team_data['logo_url']),
                'points': team_data['points'],
                'goals_scored': team_data['goals_scored'],
                'goals_conceded': team_data['goals_conceded'],
                # Add other fields as needed
                }
                new_team = self.env['team__manager.team'].create(team_vals)
                print(f"Team {team_data['name']} created.")

    
    def update_teams_from_scraped_data(self):
        # Get the scraped team data
        scraped_teams = self.scrap_teams()

        # Update or create teams based on the scraped data
        for team_data in scraped_teams:
            self.update_or_create_team(team_data)