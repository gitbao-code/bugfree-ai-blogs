---
title: "Design a File System Interview: The One Detail Candidates Keep Missing—Directory Lookups"
seoTitle: "File System Design: The Directory Lookup Detail Candidates Miss"
seoDescription: "Directory lookups make or break file system design. Learn how to model directories, resolve paths, and handle conflicts, locks, and atomic updates."
datePublished: Wed Apr 29 2026 17:16:54 GMT+0000 (Coordinated Universal Time)
cuid: cmokbhrr0000002l599ze7tku
slug: file-system-directory-lookups-missed-detail
cover: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1777482980336.png
ogImage: https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1777482980336.png

---

![Directory lookup diagram](https://bugfree-s3.s3.amazonaws.com/mermaid_diagrams/image_1777482980336.png "Directory lookup diagram")

> In file system design, the devil is in directory lookups. Every operation begins with path resolution: parse "/a/b/c", walk directories, and at each step find the next child fast and safely.

## Why a directory must not be “just a list”
A directory conceptually holds a mapping from names to nodes (files or subdirectories). If you model a directory as a naive list, every lookup becomes O(n) for the directory size — too slow for real workloads. Instead, treat a directory as a container with an efficient name → node index mapping (e.g., hash map or B-tree).

This choice affects the complexity and correctness of all higher-level operations: create, read, move, rename, and delete. Interviewers expect you to reason about lookup complexity, conflict detection, and consistency.

## Core model (simple and explicit)
- Directory: map<string, NodeIndex>
- Node: { type: file|dir, parent: NodeIndex, metadata }

Key invariants:
- Each directory contains unique names (no duplicates in one directory)
- Parent pointers are consistent (node.parent points to the directory that contains the entry)

## Path resolution: the common starting point
To operate on "/a/b/c":
1. Parse components ["a", "b", "c"].
2. Starting from the root, for each component except possibly the last, perform a directory lookup (fast map/B-tree lookup).
3. If any component lookup fails (missing component or wrong type), abort with an error.

Complexity: let k be the number of path components and L be the complexity of a single directory lookup. Total is O(k * L). With a hash map L is average O(1) (subject to hashing), with a B-tree L = O(log n).

## How core operations reduce to lookups and simple updates
- Create: resolve parent directory P, check name doesn’t exist, insert mapping name → new_node_index, set new_node.parent = P.
- Read (open/stat): resolve parent (or resolve full path), locate node, verify permissions.
- Rename/Move: resolve source parent Ps and destination parent Pd, ensure destination name doesn’t conflict, update Ps map to remove name, update Pd map to add name → same node index, update node.parent = Pd.

If you can’t explain lookup complexity and the conflict checks performed during these steps, your design is incomplete.

## Concurrency and consistency (what candidates frequently miss)
Candidates commonly forget to describe how these updates are made safe under concurrency and crashes. Important points to mention:

- Locking: use fine-grained per-directory locks (or reader/writer locks). For multi-directory ops (rename across directories), acquire locks in a global order (e.g., path lexicographic) to avoid deadlocks.
- Atomicity: perform changes in an order that preserves invariants even if a crash occurs. For example, when moving a node, add the destination entry first (or use a journal/transaction) then remove the source entry to avoid losing the node.
- Parent pointer consistency: ensure node.parent is updated in the same atomic operation as the directory mappings, or make the system tolerant of transient inconsistency until the operation commits.
- Conflict detection: always check existence and type at the resolved parent before making changes. Handle races where an entry is created between your check and your insert (use locks or atomic compare-and-swap style operations).

## Example pseudocode (rename/move)
```
function move(sourcePath, destDirPath, newName):
  srcParent, srcName = resolveParent(sourcePath)
  dstParent = resolve(destDirPath)

  acquire_locks_in_order(srcParent, dstParent)
  if not srcParent.contains(srcName): fail
  if dstParent.contains(newName): fail  # conflict check

  node = srcParent.remove(srcName)
  dstParent.insert(newName, node)
  node.parent = dstParent
  release_locks(srcParent, dstParent)
```

Discuss how to make this crash-safe (use journaling/transactions or write ordering guarantees) and how to avoid deadlock via deterministic lock ordering.

## Interview checklist — what to say out loud
- Describe your directory data structure and lookup complexity (hash map vs B-tree).
- Walk through path resolution step-by-step and show its complexity as O(k * L).
- Explain conflict checks: existence, type mismatch, permission checks.
- Describe how to keep parent pointers consistent.
- Discuss concurrency: locking strategy, deadlock avoidance, and crash recovery (journaling/transactions).
- Mention special cases: symlinks, hard links, caching, large directories (sharding), and permission/ACLs.

## TL;DR
Directories are not just lists. Model them as name → node mappings and make path resolution, lookup complexity, conflict checks, and consistency explicit. If you can't explain those pieces and how operations reduce to lookups plus a small number of updates, your file system design explanation is incomplete.

#SystemDesign #OOP #SoftwareEngineering