
# Gravity Git Standard Operating Procedures

Gravity uses the rebase strategy for working with Git and Gitlab. If you're new to this way of working and you are a visual person, you may want to check out a visualization tool so that you can see the changes and progress you make. You can find some suggestions under [Resources](#Resources)

## Table of Contents
* [Branching](#Branching)
* [Updating Your Branch](#Updating-Your-Branch)
* [Making Commits](#Making-Commits)
* [Squashing Your Commits](#Squashing-Your-Commits)
* [Making a Pull Request](#Making-a-Pull-Request)
* [Who Can Merge Your Pull Request](#Who-Can-Merge-Your-Pull-Request)
* [Deleting Branches](#Deleting-Branches)
* [Other Git Operations](#Other-Git-Operations)
* [Resources](#Resources)

## Branching

Make sure to update your master branch from the remote master branch.

Create your new branch with this naming convention:
```
<yourname>/<feature name>
```

Command line example
```
git checkout -b pfarrell/documentation-update
```

## Updating Your Branch

We use rebasing to keep our branches updated with master. Check and compare your branch frequently with the remote master and update whenever master has moved to keep your branch up to date and to minimize merge conflict issues. Ensure that your branch is also up to date even after you have made your pull request and while you are waiting for approval.

Check out your existing branch:
```
git checkout <yourname>/<featurename>
```

When updating and syncing with the mainline Git repository, we typically use the command "git fetch" to pull the latest information down from the server, then do the rebasing ourselves.  We almost never use the command "git pull" as that can cause issues.

To rebase your branch, checkout your local master and update it:
```
git fetch origin
```

Rebase on top of your local master:
```
git rebase master
```

NOTE:
When you are ready to push your local changes to your remote branch, you may run into a message that either says your branch has diverged or is behind.  You need to check if your new changes are correct and what you want to push the server. You may need to use force push in order to push your changes up to your local branch.

WARNING: Only use this command if you know what you are doing as you will overwrite information on the server.
```
git push origin <yourname>/<featurename> -f
```

## Making Commits

When you make commits, and you are in the middle of making your changes, your commit message should be typed like this:
```
in progress, <your commit message>

OR 

WIP, <your commit message>
```

Your final commit should remove the 'in progress,' part of the template above.

## Squashing Your Commits

Before making your pull request, you need to squash all your commits into one commit, making sure that your new commit message has 'in progress,' removed.

[Using GitKraken](https://support.gitkraken.com/working-with-commits/squash/)
[Using SourceTree with interactive rebase](ttps://community.atlassian.com/t5/Sourcetree-questions/In-SourceTree-how-do-I-squash-commits/qaq-p/345666)
[Using command line](https://medium.com/@slamflipstrom/a-beginners-guide-to-squashing-commits-with-git-rebase-8185cf6e62ec)

## Making a Pull Request

When making a pull request, here is a good checklist you can use as a loose guideline:
- [ ] Link to the original issue if any.
- [ ] Describe the issue you are solving
- [ ] Describe your approach to a solution
- [ ] Describe your changes
- [ ] Before vs. After. Including screenshots if applicable
- [ ] Tag a 'Merge Master' as a reviewer and other relevant users to review your code.

## Who Can Merge Your Pull Request

Only Merge Masters can merge a pull request. Pull requests will be merged using "Rebase and Merge" to keep the history tree clean and easy to follow.

## Deleting Branches

Once your branch is no longer useful or after your branch has been merged to the remote master, you may delete your branch.

## Other Git Operations

If you need to amend a commit because you recommited something from another developer:
```
git commit --amend --author="Author Name <email@address.com>"
```

## Resources

* [GitKraken](https://www.gitkraken.com/)
* [SourceTree](https://www.sourcetreeapp.com/)