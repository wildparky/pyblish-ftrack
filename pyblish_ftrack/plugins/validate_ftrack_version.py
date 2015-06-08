import pyblish.api

import ftrack

@pyblish.api.log
class ValidateFtrackVersion(pyblish.api.Validator):
    """ Validates whether ftrack version with matching version number exists

        Arguments:
            ftrackData (dictionary): Necessary ftrack information gathered by select_ftrack
    """

    families = ['*']
    hosts = ['*']
    version = (0, 1, 0)
    name = "Validate Ftrack Version"

    def process(self, instance):

        if instance.context.has_data('ftrackData'):
            assert instance.context.has_data('version'), 'Missing version in context.'
            ftrack_data = instance.context.data('ftrackData')

            if 'AssetVersion' in ftrack_data:
                asset_version = ftrack.AssetVersion(id=ftrack_data['AssetVersion']['id'])
                self.log.debug('Validating AssetVersion with ID {}'.format(ftrack_data['AssetVersion']['id']))

                if not asset_version.get('ispublished'):
                    self.log.debug("AssetVersion exists but is not visible in UI")
                    asset_version.publish()
        else:
            self.log.info('No ftrackData present. Skipping this instance')