import datetime
import sys
import aiohttp
import asyncio
from aiohttp import web

from app.models import ServicesList, ServicesStatusesList

class AddService(web.View):
    async def post(self):
        data = await self.request.json()
        if len(data['name']) < 25:
            if len(data['url']) < 1024 and len(data['des']) < 1024:
                service = await self.request.app["db"].services_list.query.where(ServicesList.name == data['name']).gino.first()
                if not(service):
                    service = await self.request.app["db"].services_list.create(
                        name = data["name"],
                        url = data["url"],
                        des = data["des"],
                    )
                    return web.json_response({
                        "text": "'" + service.name + "' added to watchlist"
                    })
                else:
                    return web.json_response({
                        "text": "'" + service.name + "' already on the watchlist"
                    })
            else:
                return web.json_response({
                    "text" : "Read the '/add' documentation"
                })
        else:
            return web.json_response({
                "text" : "Name cannot be longer than 25 characters"
            })
class StartMonitor(web.View):
    async def get(self):
        rel_url = str(self.request.rel_url).replace('/monitor/','').replace('/', '')
        if rel_url == 'start':
            if self.request.app['monitoring'] == False:
                self.request.app['monitoring'] = True
                asyncio.ensure_future(self.run_monitor(self.request.app))
                return web.json_response({
                    "text" : "Monitoring started"
                })
            else:
                return web.json_response({
                    "text" : "Monitoring already started"
                })
        elif rel_url == 'stop':
            if self.request.app['monitoring'] == False:
                return web.json_response({
                    "text" : "Monitoring already stopped"
                })
            else:
                self.request.app['monitoring'] = False
                return web.json_response({
                    "text" : "Monitoring stopped"
                })
    async def run_monitor(self,app):
        while app['monitoring']:
            await asyncio.ensure_future(self.monitor(app))
            await asyncio.sleep(1)
    async def monitor(self,app):
        services_list = await app["db"].services_list.query.where(ServicesList.id >= 0).gino.all()
        async with aiohttp.ClientSession() as session:
            for service in services_list:
                status = await self.get_service_status(session, service.url)
                service_status = await app["db"].services_statuses_list.create(
                    id = service.id,
                    status = status,
                    datetime = datetime.datetime.now()
                )
    async def get_service_status(self,session, url):
        async with session.get(url) as resp:
            return resp.status
class History(web.View):
    async def get(self):
        services_list = await self.request.app["db"].services_list.query.where(ServicesList.id >= 0).gino.all()
        full_res = {}
        for service in services_list:
            res = {}
            services_statuses_list = await self.request.app["db"].services_statuses_list.query.where(ServicesStatusesList.id == service.id).gino.all()
            for service_status in services_statuses_list:
                res.update({str(service_status.datetime) : service_status.status})
            full_res.update({ service.name : res})
        return web.json_response(full_res)
class LastStatuses(web.View):
    async def get(self):
        services_list = await self.request.app["db"].services_list.query.where(ServicesList.id >= 0).gino.all()
        full_res = {}
        for service in services_list:
            services_statuses_list = await self.request.app["db"].services_statuses_list.query.where(ServicesStatusesList.id == service.id).gino.all()
            if len(services_statuses_list) > 0:
                counter = 0
                for i in services_statuses_list:
                    if 300 > i.status >= 200:
                        counter += 1
                sla = counter / len(services_statuses_list)
                full_res.update({ service.name : { 'URL' : service.url ,'status' : services_statuses_list[-1].status, 'last_update' : str(services_statuses_list[-1].datetime), 'SLA' : str(round(sla*100,3))+"%", 'Description' : service.des }})
        return web.json_response(full_res)
class Interval(web.View):
    async def post(self):
        data = await self.request.json()
        format = '%Y-%m-%d %H:%M:%S.%f'
        service = await self.request.app["db"].services_list.query.where(ServicesList.name == data["service_name"]).gino.first()
        if service:
            try:
                start_datetime = datetime.datetime.strptime(data["start"], format)
                end_datetime = datetime.datetime.strptime(data["end"], format)
                services_statuses_list = await self.request.app["db"].services_statuses_list.query.where(ServicesStatusesList.id == service.id).gino.all()
                res = {}
                for service_status in services_statuses_list:
                    if start_datetime <= service_status.datetime <= end_datetime:
                        res.update({ str(service_status.datetime) : service_status.status})
                return web.json_response({ service.name : res})
            except:
                return web.json_response({
                    "text" : "The start and end fields must contain datetime objects in the format: "+format
                })
        else:
            return web.json_response({
                "text" : "This service is not on the watch list. Read the '/add' documentation. "
            })

class ClearAllTables(web.View):
    async def get(self):
        await self.request.app["db"].services_list.delete.where(ServicesList.id < 100000000).gino.status()
        await self.request.app["db"].services_statuses_list.delete.where(ServicesStatusesList.id < 100000000).gino.status()
        return web.json_response({'status': 'OK'})