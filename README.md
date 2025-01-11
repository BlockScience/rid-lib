# RID v3 Protocol

*This specification can be understood as the third iteration of the RID protocol, or RID v3. Previous versions include [RID v1](https://github.com/BlockScience/kms-identity/blob/main/README.md) and [RID v2](https://github.com/BlockScience/rid-lib/blob/v2/README.md).*

### Jump to Sections: 
 - [RID Core](#rid-core)
	- [Introduction](#introduction)
	- [Generic Syntax](#generic-syntax)
	- [Object Reference Names](#object-reference-names-previously-rid-v2)
	- [Implementation](#implementation) 
	- [Installation](#installation)
	- [Usage](#usage)
	- [Development](#development)
 - [RID Extensions](#rid-extensions)

# RID Core
## Introduction

*Note: throughout this document the terms "resource", "digital object", and "knowledge object" are used roughly interchangeably.*

Reference Identifiers (RIDs) identify references to resources primarily for usage within Knowledge Organization Infrastructure (KOI). The RID specification is informed by previous work on representing digital objects (see [Objects as Reference](https://blog.block.science/objects-as-reference-toward-robust-first-principles-of-digital-organization/)) in which objects are identified through a relationship between a reference and a referent. Under this model, RIDs are the *references*, and the resources they refer to are the *referents.* The *means of reference* describes the relationship between the reference and referent.

```
(reference) -[means of reference]-> (referent)
```

As opposed to Uniform Resource Identifiers (URIs), RIDs are not intended to have universal agreement or a centralized management structure. However, RIDs are compatible with URIs in that *all URIs can be valid RIDs*. [RFC 3986](https://www.rfc-editor.org/info/rfc3986) outlines the basic properties of an URI, adding that "a URI can be further classified as a locator, a name or both." Location and naming can be considered two different means of reference, or methods of linking a reference and referent(s), where:

1. Locators identify resources by *where* they are, with the referent being defined as the resource retrieved via a defined access method. This type of identifier is less stable, and the resource at the specified location could change or become unavailable over time.
3. Names identify resources by *what* they are, acting as a more stable, location independent identifier. Resources identified by name are not always intended to be accessed, but some may be resolvable to locators. While the mapping from name to locator may not be constant the broader relationship between reference and referent should be.
## Generic Syntax

The generic syntax to compose an RID roughly mirrors URIS:
```
<context>:<reference>
```

Conceptually, the reference refers to the referent, while the context provides context for how to interpret the reference, or how to discriminate it from another otherwise identical RID. While in many cases the context simply maps to a URI scheme, the context may also include part of the "hierarchical part" (right hand side of a URI following the scheme).
## Object Reference Names (previously RID v2)

The major change from RID v2 to v3 was building compatibility with URIs, and as a result the previous RID v2 style identifiers are now implemented under the (unofficial) `orn:` URI scheme. 

Object Reference Names (ORNs) identify references to objects, or resources identified independent of their access method. Given the previous definitions of identifiers, ORNs can be considered "names". They are intended to be used with existing resources which may already have well defined identifiers. An ORN identifies a resource by "dislocating" it from a specific access mechanism, maintaining a reference even if the underlying locator changes or breaks. ORNs are generally formed from one or more context specific identifiers which can be easily accessed for processing in other contexts.

ORNs are composed using the following syntax:
```
orn:<namespace>:<reference>
```
*Note: In previous versions, the namespace was split into `<space>.<form>`. Using a dot to separate a namespace in this way is still encouraged, but is not explicitly defined by this specification.*

ORNs also implement a more complex context component: `orn:<namespace>`. The differences between the syntax of ORNs and generic URIs are summarized here:
```
<scheme>:<hierarchical-part>
\______/ \_________________/
    |                |
 context         reference
 ___|_________   ____|____
/             \ /         \
orn:<namespace>:<reference>
```

## Examples

In the current version there are two example implementations of RID types: HTTP/S URLs and Slack objects. The HTTP/S scheme is the most commonly used form of URI and uses the standard RID parsing, where the scheme `http` or `https` is equal to the context, and the hierarchical part is equal to the reference. 

```
scheme  authority                  path
 _|_     ____|___  _________________|___________________
/   \   /        \/                                     \
https://github.com/BlockScience/rid-lib/blob/v3/README.md
\___/ \_________________________________________________/
  |                           |
context                   reference
```

The Slack objects are implemented as ORNs, and include workspaces, channels, messages, and users. The Slack message object's namespace is `slack.message` and its reference component is composed of three internal identifiers, the workspace id, channel id, and message id.

```
scheme namespace     team      channel      timestamp
 |   _____|_____   ___|___    ____|___   _______|_______
/ \ /           \ /       \ /         \ /               \
orn:slack.message:TA2E6KPK3/C07BKQX0EVC/1721669683.087619
\_______________/ \_____________________________________/
        |                            |
     context                     reference
```

By representing Slack messages through ORNs, a stable identifier can be assigned to a resource which can be mapped to existing locators for different use cases. For example, a Slack message can be represented as a shareable link which redirects to the Slack app or in browser app: 
```
https://blockscienceteam.slack.com/archives/C07BKQX0EVC/p1721669683087619`
```
There's also a "deep link" which can open the Slack app directly (but only to a channel):
```
slack://open?team=TA2E6KPK3&id=C07BKQX0EVC
```
Finally, there's the backend API call to retrieve the JSON data associated with the message:
```
https://slack.com/api/conversations.replies?channel=C07BKQX0EVC&ts=1721669683.087619&limit=1
```
These three different locators have specific use cases, but none of them work well as long term identifiers of a Slack message. None of them contain all of the identifiers needed to uniquely identify the message (the shareable link comes close, but uses the mutable team name instead of the id). Even if a locator can fully describe an object of interested, it is not resilient to changes in access method and is not designed for portability into systems where the context needs to be clearly stated and internal identifiers easily extracted. Instead, we can represent a Slack message as an ORN and resolve it to any of the above locators when necessary.

## Implementation

The RID class provides a template for all RID types and access to a global constructor. All RID instances have access to the following properties:
```python
scheme: str

# defined for ORNs only
namespace: str | None 

# "orn:<namespace>" for ORNs, otherwise equal to 'scheme'
context: str

# the component after namespace component for ORNs, otherwise after the scheme component
reference: str
```
and the following methods:
```python
@classmethod
def from_string(cls, string: str, allow_prov_ctx=True) -> RID: ... 

# only callable from RID type classes, not the RID base class
@classmethod
def from_reference(cls, string: str) -> RID: ...
```

In order to create an RID type, follow this minimal implementation:
```python
class TypeName(RID | ORN): # inherit from RID OR ORN base classe
	# define scheme for a generic URI type
	scheme = "scheme"
	# OR a namespace for a ORN type
	namespace = "namespace"

	# instantiates a new RID from internal components
	def __init__(self, internal_id):
		self.internal_id = internal_id
	
	# returns the reference component
	@property
	def reference(self):
		# should dynamically reflect changes to any internal ids
		return self.internal_id
	
	# instantiates of an RID of this type given a reference
	@classmethod
	def from_reference(cls, reference):
		# in a typical use case, the reference would need to be parsed
		return cls(reference)
```

[Example implementations can be found here.](https://github.com/BlockScience/rid-lib/tree/v3/src/rid_lib/types)

## Installation

This package can be installed with pip for use in other projects.
```
pip install rid-lib
```

It can also be built and installed from source by cloning this repo and running this command in the root directory.
```
pip install .
```

## Usage

RIDs are intended to be used as a lightweight, cross platform identifiers to facilitate communication between knowledge processing systems. RID objects can be constructed from any RID string using the general constructor `RID.from_string`. The parser will match the string's context component and call the corresponding `from_reference` constructor. This can also be done directly on any context class via `Context.from_reference`. Finally, each context class provides a default constructor which requires each subcomponent to be indvidiually specified.
```python
from rid_lib import RID
from rid_lib.types import SlackMessage

rid_obj1 = RID.from_string("orn:slack.message:TA2E6KPK3/C07BKQX0EVC/1721669683.087619")
rid_obj2 = SlackMessage.from_reference("TA2E6KPK3/C07BKQX0EVC/1721669683.087619")
rid_obj3 = SlackMessage(team_id="TA2E6KPK3", channel_id="C07BKQX0EVC", ts="1721669683.087619")

assert rid_obj1 == rid_obj2 == rid_obj3

# guaranteed to be defined for all RID objects
print(rid_obj1.scheme, rid_obj1.context, rid_obj1.reference)

# special parameters for the slack.message context
print(rid_obj1.team_id, rid_obj1.channel_id, rid_obj1.ts)
```

If an RID type hasn't been implemented as a context class, it can still be parsed by the general constructor if provisional contexts are allowed (enabled by default). In this case a provisional context class is generated on the fly providing the minimal RID type implementation (`reference` property, `from_reference` class method, `__init__` function).

```python
test_obj1 = RID.from_string("test:one")
test_obj2 = RID.from_string("test:one")

assert test_obj1 == test_obj2
```

## Development

Build and install from source with development requirements:
```
pip install .[dev]
```
Run unit tests:
```
pytest --cov=rid_lib
```
To build and upload to PyPI:
(Remember to bump the version number in pyproject.toml first!)
```
python -m build
```
Two new build files should appear in `dist/`, a `.tar.gz` and `.whl` file.
```
python -m twine upload --repository pypi dist/*
```
Enter the API key and upload the new package version.

# RID Extensions
## Introduction
In addition to the core implementation of the RID specification, this library also provides the extended functionality of objects and patterns that interface with RIDs. These features require optional dependencies to properly function, which is specified after the package name:
```
pip install rid-lib[ext]
```

## Manifest
A manifest is a portable descriptor of a data object associated with an RID. It is composed of an RID and metadata about the data object it describes(currently a timestamp and sha256 hash). The name "manifest" comes from a shipping metaphor: a piece of cargo has contents (the stuff inside of it) and a manifest (a paper describing the contents and providing tracking info). In the KOI network ecosystem, a manifest serves a similar role. Manifests can be passed around to inform other nodes of a data objects they may be interested in.

Below are the accessible fields and methods of a Manifest object, all are required.

```python
class Manifest:
	rid: RID
	timestamp: datetime
	sha256_hash: str

	# creates a new Manifest with the provided fields
	def __init__(
		self, 
		rid: RID, 
		timestamp: datetime, 
		sha256_hash: str
	): ...

	# generates a Manifest using the current datetime and the hash of the provided data
	@classmethod
	def generate(cls, rid: RID, data: dict) -> Manifest: ...

	# JSON serialization functions
	@classmethod
	def from_json(cls, data: dict) -> Manifest: ...
	def to_json(self) -> dict: ...
```
## Event
An event is a signalling construct that conveys information about RID objects between networked nodes. In this version of the network, this signalling path will be `sensor -> coordinator -> processor`. Events are generated by sensors upon discovering a new knowledge object, an update to an existing knowledge object, or a knowledge object was deleted or should be forgotten by the network. These scenarios correspond to the three (FUN) event types:

- FORGET
- UPDATE
- NEW

As opposed to CRUD (create, read, update, delete), FUN is a series of messages, not operations. Each node has its own autonomy in deciding how to react based on the message it receives. For example, a processor node may receive a "new" event for an RID object its not interested in, and ignore it. Or it may decide that an "update" event should trigger a dereference call to a sensor to retrieve an updated version of an RID's data.

An event object is composed of an RID, an event type, and an optional manifest. Below are the accessible fields and methods of an Event object. 

```python
class Event:
    rid: RID
	# one of the FUN types
    event_type: str 
    manifest: Manifest | None
	
	# creates a new Event with the provided fields
	def __init__(
		self, 
		rid: RID, 
		event_type: str, 
		manifest: Manifest | None = None
	): ...

	# JSON serialization functions
	@classmethod
	def from_json(cls, data: dict) -> Event: ...
	def to_json(self) -> dict: ...
```

## Cache
The cache module provides two functions: a basic cache interface for storing data objects associated with RIDs, and a portable 'cache bundle' data format for storing and transferring these objects.

A cache bundle is composed of a manifest and (optional) contents. This is the "piece of cargo" in the shipping metaphor described above. It's the construct used to transfer and store the RIDed knowledge objects we are interested in. The contents are optional to allow just the manifests to be cached by themselves. Below are the accessible fields and methods of an Event object.

```python
class CacheBundle:
    manifest: Manifest
    contents: dict | None

	# create a new CacheBundle with the provided fields
	def __init__(
		self, 
		manifest: Manifest, 
		contents: dict | None = None
	): ...

	# JSON serialization functions
	@classmethod
	def from_json(cls, data: dict) -> CacheBundle: ...
	def to_json(self) -> dict: ...
```

The cache interface allows us to set up a cache for reading and writing these cache bundles. Each cache bundle is stored as a separate JSON file in the cache directory, where the file name is base 64 encoding of its RID. Below are the accessible fields and methods of a Cache.

```python
class Cache:
	directory_path: str

	# sets up a new cache under the provided directory
    def __init__(self, directory_path: str): ...  

	# provides the path to the cache entry of the provided RID
    def file_path_to(self, rid: RID) -> str: ...

	# WRITE METHODS
	# writes a cache bundle
    def write(self, rid: RID, cache_bundle: CacheBundle) -> CacheBundle: ...
	# creates a cache bundle from the provided data (Manifest.generate) and writes it
    def bundle_and_write(self, rid: RID, data: dict) -> CacheBundle: ...
	# creates a cache bundle from the provided manifest and writes it
    def write_manifest_only(self, rid: RID, manifest: Manifest) -> CacheBundle: ...

	# READ METHODS
	# returns whether a cache entry exists for the provided RID
    def exists(self, rid: RID) -> bool: ...
	# returns cache bundle of provided RID (or None if it doesn't exist)
    def read(self, rid: RID) -> CacheBundle | None: ...
	# returns a list of all of the RIDs currently cached
    def read_all_rids(self) -> list[RID]: ...

	# DELETE METHODS
	# deletes the cache entry of the provided RID
    def delete(self, rid: RID) -> None: ...
	# wipes the cache completely
    def drop(self) -> None: ...
```

## Effector

The effector is the most abstract construct out of the rid-lib extensions. It acts as an "end effector", performing actions on/with RIDs. More concretely, it allows you to define and bind functions to a specific action type and RID context. The most obvious use case for this is as a dereferencer (and this use case has added functionality): a dereference function can be defined for different types of RIDs, and the effector will automatically choose the correct one to run based on the context of the RID passed in. Below are the accessible fields and methods of Effector.

```python
class Effector:
	cache: Cache | None

	# alias to 'execute', allows actions to be run by calling:
	# effector.run.<action_type>(rid: RID, *args, **kwargs)
	run: ProxyHandler

    def __init__(self, cache: Cache | None = None): ...
    
	# decorator used to register actions to the effector:
	# @effector.register(action_type, rid_type)
    def register(
        self, 
        action_type: ActionType, 
		# rid_type may be singular or multiple strings or RID type classes
        rid_type: Type[RID] | str | tuple[Type[RID] | str]
    ): ...
    
	# decorator used to register dereference actions to the effector
	# (alias to 'register', sets action_type=ActionType.dereference)
    def register_dereference(
		self, 
		rid_type: Type[RID] | str | tuple[Type[RID] | str]
	): ...

	def execute(
		self, 
		action_type: str, 
		rid: RID, 
		*args, 
		**kwargs
	): ...

	# special handler for 'dereference' actions, returns a CacheBundle instead of dict, optionally interacts with cache
	# note: different behavior than calling 'dereference' action with 'execute' or 'run'
    def deref(
        self, 
        rid: RID, 
        hit_cache=True, # tries to read cache first, writes to cache if there is a miss
        refresh=False   # refreshes cache even if there was a hit
    ) -> CacheBundle | None: ...

```

Registering and calling actions with an Effector:

```python
import requests
from rid_lib import RID
from rid_lib.ext import Cache, Effector, ActionType
from rid_lib.types import HTTP, HTTPS

cache = Cache("my_cache")
effector = Effector(cache)

@effector.register_dereference((HTTP, HTTPS))
def dereference_url(url):
	return requests.get(str(url)).json()

my_url = RID.from_string("https://jsonplaceholder.typicode.com/todos/1")

# equivalent actions, returns dict
effector.execute(ActionType.dereference, url)
effector.execute("dereference", url)
effector.run.dereference(url)

# special dereference handler, returns CacheBundle
effector.deref(url)
effector.deref(url, hit_cache=False)
effector.deref(url, refresh=True)
```