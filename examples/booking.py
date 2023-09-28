import json
import os
from typing import Annotated

import typer

import clisk

from clisk.arguments import *

clisk.set_up(help='A simple tool to manage bookings and clients.', add_completion=False)
clisk.intermediate('create', help='Create a new object.')
clisk.intermediate('delete', help='Delete the object.')
clisk.intermediate('get', help='List the objects.')


@clisk.command('create', 'client', help='Create a new client profile.')
def cmd_create_client(
        clients_dir: arg_writable_path('Directory containing the clients files.'),
        name: Annotated[str, typer.Argument(help='Name of the client.')],
        email: Annotated[str, typer.Argument(help='Email fo the client.')]
):
    client_file = clients_dir / (name + '.json')
    if client_file.exists():
        raise FileExistsError(f'A client with the name {name} already exists.')

    client_file.write_text(json.dumps({'name': name, 'email': email}))


@clisk.command('create', 'booking', help='Create a new booking.')
def cmd_create_booking(
        bookings_dir: arg_writable_path('Directory containing the bookings files.'),
        client_name: Annotated[str, typer.Argument(help='Name of the client.')],
        arrival_date: Annotated[str, typer.Option(help='Date of arrival.')],
        departure_date: Annotated[str, typer.Option(help='Date of departure.')]
):
    booking_file = bookings_dir / (arrival_date + '-' + departure_date + '.json')
    booking_file.write_text(json.dumps({
        'client': client_name,
        'arrival': arrival_date,
        'departure': departure_date
    }))


@clisk.command('delete', 'client', help='Delete the client.')
def cmd_delete_client(
        clients_dir: arg_writable_path('Directory containing the clients files.'),
        name: Annotated[str, typer.Argument(help='Name of the client.')],
):
    client_file = clients_dir / (name + '.json')
    if not client_file.exists():
        raise FileNotFoundError(f'The client {name} was not found.')

    os.remove(client_file)


@clisk.command('delete', 'booking', help='Delete the booking.')
def cmd_delete_client(
        bookings_dir: arg_writable_path('Directory containing the bookings files.'),
        arrival_date: Annotated[str, typer.Option(help='Date of arrival.')],
        departure_date: Annotated[str, typer.Option(help='Date of departure.')]
):
    booking_file = bookings_dir / (arrival_date + '-' + departure_date + '.json')
    if not booking_file.exists():
        raise FileNotFoundError(f'The booking {booking_file.stem} was not found.')

    os.remove(booking_file)


@clisk.command('get', 'client', help='List the known clients.')
def cmd_get_clients(
        clients_dir: arg_writable_path('Directory containing the clients files.')
):
    print('Known clients:')
    for client_file in clients_dir.glob('./*.json'):
        data = json.loads(client_file.read_text())
        print(f'- {data["name"]} ({data["email"]})')


@clisk.command('get', 'booking', help='List the registered bookings.')
def cmd_get_bookings(
        bookings_dir: arg_writable_path('Directory containing the bookings files.'),
):
    print('Registered bookings:')
    for booking_file in bookings_dir.glob('./*.json'):
        data = json.loads(booking_file.read_text())
        print(f'- {data["arrival"]} to {data["departure"]}: {data["client"]}')


if __name__ == '__main__':
    clisk.run()
