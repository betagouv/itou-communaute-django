# La communauté de l'inclusion

## Poetry

### Lancer le serveur local

#### Configuration environnement

```bash
$ cp .env.template .env
```

Installation des dependances avec Poetry
```bash
$ poetry install
```

#### Lancement

Pour utiliser les commandes python dans l'environnement géré par `poetry`

* Ajoutez la variable d'environnement : `DJANGO_SETTINGS_MODULE` pour activer les settings de prod (`config.settings.base`) ou de dev (`config.settings.dev`)
* Lancer le shell `poetry shell`
* Puis executer les commandes du fichier `Makefile`
```bash
$ make server
```

* Ou les commandes python de votre choix : ie `pytest`. Executées depuis le `shell` de `poetry`, cette commande équivaut à `poetry run pytest`
* Bonus, les tests lancés depuis `vscode` avec `pytest` bénéficient aussi de tout l'environnement `poetry`

### Ajout de dépendance

Ajout d'une dépendance :

```bash
poetry add django-anymail
```

Ajout d'une dépendance de développement :

```bash
poetry add --group dev poethepoet
```

### Mise à jour des dépendances

```bash
poetry update
poetry lock
```

### Générer les fichiers `requirements`

```bash
poetry run poe export
poetry run poe export_dev
```

### Déboguer pas à pas

Le débogueur démarre par défaut avec `debugpy`.

Il vous reste juste à configurer votre IDE pour qu'il s'y attache. Dans VSCode, il suffit de créer le fichier `launch.json` dans le répertoire `.vscode` comme suit :

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Django with venv",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver"
            ],
            "django": true,
            "justMyCode": true
        }
    ]
}

```

Vous pourrez dès lors placer des points d'arrêt dans le code en survolant le numéro de ligne dans la colonne à gauche et de lancer le débogueur (qui ne fera que s'attacher au serveur de deboguage qui tourne dans votre conteneur).

## Docker


### Lancer le serveur local

```bash
$ cp .env.template .env
```

Pour Docker, mettre : `POSTGRESQL_ADDON_HOST=postgres`.

```bash
$ docker-compose up -d
```

Visitez la page d'accueil du projet : http://localhost:8000.

Si le port 8000 ne vous convient pas, vous pouvez définir la variable `DJANGO_PORT_ON_DOCKER_HOST` dans votre `.env` pour mettre le port que vous souhaitez.

### Déboguer pas à pas

Le débogueur démarre par défaut avec `debugpy` dans le conteneur Django sur le port 5678 (que vous pouvez changer avec la variable d'environnement `DJANGO_DEBUGPY_PORT`).
Il vous reste juste à configurer votre IDE pour qu'il s'y attache. Dans VSCode, il suffit de créer le fichier `launch.json` dans le répertoire `.vscode` comme suit :

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Attacher",
            "type": "python",
            "request": "attach",
            "connect": {
                "host": "127.0.0.1",
                "port": 5678
            },
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ],
            "django": true
        }
    ]
}
```

Vous pourrez dès lors placer des points d'arrêt dans le code en survolant le numéro de ligne dans la colonne à gauche et de lancer le débogueur (qui ne fera que s'attacher au serveur de deboguage qui tourne dans votre conteneur).

## Créer rapidement des forums privés dans le shell

### chargement des modèles

```
from django.contrib.auth.models import Group
from machina.core.db.models import get_model
from machina.core.loading import get_class
Forum = get_model("forum", "Forum")
ForumPermission = get_model("forum_permission","ForumPermission")
UserForumPermission = get_model("forum_permission","UserForumPermission")
GroupForumPermission = get_model("forum_permission","GroupForumPermission")
```

### creation du forum et des groupes
La variable `name` contient le nom du forum privé à créer.
```
name = 'nom du forum privé'
```

```
moderators, _ = Group.objects.get_or_create(name=f"{name} moderators")
members, _ = Group.objects.get_or_create(name=f"{name} members")
forum, _ = Forum.objects.get_or_create(name=name,is_private=True,members_group=members,type=0)
```

### ajouter les droits pour les utilisateurs anonymes
```
UserForumPermission.objects.bulk_create(
    [UserForumPermission(anonymous_user=True,authenticated_user=False,permission=permission,has_perm=False,forum=forum) for permission in ForumPermission.objects.all()
    ]
)
```

### ajouter les droits pour les utilisateurs authentifiés
```
UserForumPermission.objects.bulk_create(
    [UserForumPermission(anonymous_user=False,authenticated_user=True,permission=permission,has_perm=False,forum=forum) for permission in ForumPermission.objects.all()
    ]
)
```

### ajouter les permissions du groupe moderators
```
GroupForumPermission.objects.bulk_create(
    [GroupForumPermission(group=moderators,permission=permission,has_perm=True,forum=forum) for permission in ForumPermission.objects.all()

    ]
)
```

### ajouter les permissions du groupe members
```
declined = ['can_edit_posts', 'can_lock_topics', 'can_delete_posts', 'can_move_topics', 'can_approve_posts', 'can_reply_to_locked_topics', 'can_vote_in_polls', 'can_create_polls', 'can_post_stickies', 'can_post_announcements']
GroupForumPermission.objects.bulk_create(
    [GroupForumPermission(group=members,permission=permission,has_perm=False,forum=forum) for permission in ForumPermission.objects.filter(codename__in=declined)
    ]
)
GroupForumPermission.objects.bulk_create(
    [GroupForumPermission(group=members,permission=permission,has_perm=True,forum=forum) for permission in ForumPermission.objects.exclude(codename__in=declined)
    ]
)
```

## Utiliser les factories de `machina`

### créer un forum

```
from machina.test.factories.forum import create_forum
forum = create_forum(name="forum 1")
```

### créer des topics et des posts dans un forum

```
from machina.test.factories.conversation import PostFactory, TopicFactory

from machina.core.db.models import get_model
Topic = get_model("forum_conversation", "Topic")

topics = TopicFactory.create_batch(10, forum=forum, poster=user, type=Topic.TOPIC_POST)
posts =  (PostFactory.create_batch(5, topic=topic, poster=user) for topic in topics)
```

### Ajouter les permissions à l'utilisateur pour lire le forum

```
from machina.test.factories.permission import UserForumPermissionFactory

from machina.core.db.models import get_model
ForumPermission = get_model("forum_permission", "ForumPermission")
UserForumPermission = get_model("forum_permission", "UserForumPermission")

UserForumPermissionFactory(
    permission=ForumPermission.objects.get(codename="can_see_forum"),
    forum=forum,
    user=user,
    has_perm=True,
    )
UserForumPermissionFactory(
    permission=ForumPermission.objects.get(codename="can_read_forum"),
    forum=forum,
    user=self.user,
    has_perm=True,
    )
```

## Reinitialiser les tokens d'invitation et attribuer un groupe de membres à chaque forum

```
import uuid
from django.contrib.auth.models import Group
from lacommunaute.forum.models import Forum
forums = Forum.objects.all()
for forum in forums:
    forum.invitation_token = uuid.uuid4()
    group,_ =Group.objects.get_or_create(name=f'{forum.name} members')
    forum.members_group = group
    forum.save()
```
