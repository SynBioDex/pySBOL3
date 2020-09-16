Biological Parts Repositories
=============================

-----------------------------------------------
Re-using Genetic Parts From Online Repositories
-----------------------------------------------

In today's modern technological society, a variety of interesting technologies can be assembled from 
"off-the-shelf" components, including cars, computers, and airplanes. Synthetic biology is inspired by a similar idea. Synthetic biologists aim to program new biological functions into organisms by assembling genetic code from off-the-shelf DNA sequences. PySBOL2 puts an inventory of biological parts at your fingertips.

For example, the `iGEM Registry of Standard Biological Parts <http://parts.igem.org/Main_Page>`_ is an online resource that many synthetic biologists are familiar with.  The Registry is an online database that catalogs a vast inventory of genetic parts, mostly contributed by students in the iGEM competition. These parts are now available in SBOL format in the `SynBioHub <https://synbiohub.org>`_ knowledgebase, hosted by Newcastle University. The code example below demonstrates how a programmer can access these data.

The following code example shows how to pull data about biological components from the SynBioHub repository. In order to pull a part, simply locate the web address of that part by browsing the SynBioHub repository online. Alternatively, pySBOL2 also supports programmatic querying of SynBioHub (see below).

The interface with the SynBioHub repository is represented by a ``PartShop`` object. The following code retrieves parts corresponding to promoter, coding sequence (CDS), ribosome binding site (RBS), and transcriptional terminator. These parts are imported into a ``Document`` object, which must be initialized first. See `Getting Started with SBOL <getting_started.html>`_ for more about creating ``Documents``. A Uniform Resource Identifier (URI) is used to retrieve objects from the ``PartShop``, similar to how URIs are used to retrieve objects from a ``Document`` 

.. code:: python

    >>> igem = PartShop('https://synbiohub.org')
    >>> igem.pull('https://synbiohub.org/public/igem/BBa_R0010/1', doc)


.. end

Typing full URIs can be tedious. Therefore the ``PartShop`` interface provides a shortcut for retrieving objects. It will automatically construct a URI from the ``PartShop`` namespace and the part's ``displayId``. Constrast the above with the following.

.. code:: python

    >>> igem = PartShop('https://synbiohub.org/public/igem')
    >>> igem.pull('BBa_B0032', doc)
    >>> igem.pull('BBa_E0040', doc)
    >>> igem.pull('BBa_B0012', doc)


.. end

The ``pull`` operation will retrieve ``ComponentDefinitions`` and their associated ``Sequence`` objects.

.. code:: python

    >>> for obj in doc:
    ...     print(obj)
    ...
    https://synbiohub.org/public/igem/igem2sbol/1
    https://synbiohub.org/public/igem/BBa_R0010_sequence/1
    https://synbiohub.org/public/igem/BBa_R0010/1
    https://synbiohub.org/public/igem/BBa_B0032/1
    https://synbiohub.org/public/igem/BBa_B0032_sequence/1
    https://synbiohub.org/public/igem/BBa_E0040_sequence/1
    https://synbiohub.org/public/igem/BBa_E0040/1
    https://synbiohub.org/public/igem/BBa_B0012_sequence/1
    https://synbiohub.org/public/igem/BBa_B0012/1

.. end

--------------------
Logging in to Part Repos
--------------------

Some parts repositories can be accessed as above, without
authenticating to the parts repository. You may also have access to
additional parts at some parts repositories if you authenticate to the
repository. This can be done with a few more lines of code when
creating your ``PartShop``. Here is an example of how to
add authentication when using a ``PartShop``:

.. code:: python

    import sbol2
    PART_SHOP_USER = 'your_username'
    PART_SHOP_PASSWORD = 'your_password'
    part_shop = sbol2.PartShop('https://synbiohub.org')
    part_shop.login(PART_SHOP_USER, PART_SHOP_PASSWORD)


--------------------
Searching Part Repos
--------------------

PySBOL2 supports three kinds of searches: a **general search**, an **exact search**, and an **advanced search**.

The following query conducts a **general search** which scans through `identity`, `name`, `description`, and `displayId` properties for a match to the search text, including partial, case-insensitive matches to substrings of the property value. Search results are returned as a list.

.. code:: python

    records = igem.search('plasmid')
.. end

By default, the general search looks only for ``ComponentDefinitions``, and only returns 25 records at a time in order to prevent server overload. The search above is equivalent to the one below, which explicitly specifies which kind of SBOL object to search for, an offset of 0 (explained below), and a limit of 25 records.

.. code:: python

    records = igem.search('plasmid', SBOL_COMPONENT_DEFINITION, 0, 25)
.. end

Of course, these parameters can be changed to search for different type of SBOL objects or to return more records. For example, some searches may match a large number of objects, more than the specified limit allows. In this case, it is possible to specify an offset and to retrieve additional records in successive requests. The total number of objects in the repository matching the search criteria can be found using the searchCount method, which has the same call signature as the search method. It is a good idea to put a small delay between successive requests to prevent server overload. The following example demonstrates how to do this. As of the writing of this documentation, this call retrieves 391 records.

.. code:: python

    import time

    records = []
    search_term = 'plasmid'
    limit = 25
    total_hits = igem.searchCount(search_term)
    for offset in range(0, total_hits, limit):
        records.extend( igem.search(search_term, SBOL_COMPONENT_DEFINITION, offset, limit) )
        time.sleep(0.1)
.. end

The list returned by ``search`` contains multiple records. Each record contains basic data, including identity, displayId, name, and description fields. *It is very important to realize however that the search does not retrieve the complete ComponentDefinition!* In order to retrieve the full object, the user must call ``pull`` while specifying the target object's identity.

Records returned by ``search`` have an ``identity`` attribute that can be used when calling ``pull``:

.. code:: python

    for record in records:
        print(record.identity)
.. end

The preceding examples concern **general searches**, which scan through an object's metadata for partial matches to the search term. In contrast, the **exact search** explicitly specifies which property of an object to search, and the value of that property must exactly match the search term. The following **exact search** will search for ``ComponentDefinitions`` with a role of promoter:

.. code:: python

    records = igem.search(SO_PROMOTER, SBOL_COMPONENT_DEFINITION, SBOL_ROLES, 0, 25);
.. end

*Note: advanced search is not yet implemented in pySBOL2.*
*This documentation describes how it works in pySBOL.*

Finally, the **advanced search** allows the user to configure a search with multiple criteria by constructing a ``SearchQuery`` object. The following query looks for promoters that have an additional annotation indicating that the promoter is regulated (as opposed to constitutive):

.. code:: python

    q = SearchQuery();
    q['objectType'].set(SBOL_COMPONENT_DEFINITION);
    q['limit'].set(25);
    q['offset'].set(0);
    q['role'].set(SO_PROMOTER);
    q['role'].add('http://wiki.synbiohub.org/wiki/Terms/igem#partType/Regulatory');
    total_hits = igem.searchCount(q);
    records = igem.search(q);
.. end

----------------------------
Submitting Designs to a Repo
----------------------------

Users can submit their SBOL data directly to a ``PartShop`` using the pySBOL2 API. This is important, so that  synthetic biologists may reuse the data and build off each other's work. Submitting to a repository is also important for reproducing published scientific work. The synthetic biology journal ACS Synthetic Biology now encourages authors to submit SBOL data about their genetically engineered DNA to a repository like `SynBioHub <https://synbiohub.org>`__. In order to submit to a ``PartShop`` remotely, the user must first vist the appropriate website and register. Once the user has established an account, they can then log in remotely using pySBOL2.

.. code:: python

    >>> igem.login('johndoe@example.org', password)


.. end

Upon submission of a ``Document`` to SynBioHub, the ``Document`` will be converted to a ``Collection``. Therefore, the ``Document`` requires that the ``displayId``, ``name``, and ``description``  properties are set prior to submission.

.. code:: python

    >>> doc.displayId = 'my_collection'
    >>> doc.name = 'my collection'
    >>> doc.description = 'a description of your collection'
    >>> igem.submit(doc)

.. end

Once uploaded, a new URI for the ``Collection`` is generated. This URI follows the pattern ``<PART SHOP URI>/<USER NAME>/<DOCUMENT DISPLAYID>_collection``.  Other ``TopLevel`` objects in the ``Document`` are also mapped to new URIs.  These URIs follow the pattern ``<PART SHOP URI>/<USER NAME>/<SBOL TYPE>_<DISPLAYID>``.

After submission, it is possible to attach other types of data files to SBOL objects. This requires the new URI of the target object and a path to the local file on the user's machine.

.. code:: python

    >>> igem.attachFile('<PART SHOP URI>/<USER NAME>/<SBOL TYPE>_<DISPLAYID>', '<PATH TO LOCAL FILE>')


.. end

Likewise, it is possible to download a file attachment.

.. code:: python

    >>> igem.downloadAttachment('<PART SHOP URI>/<USER NAME>/<SBOL TYPE>_<DISPLAYID>', '<PATH TO WRITE>')


.. end
